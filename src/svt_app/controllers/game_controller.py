"""Game controller module for Révijouer application."""

from typing import Dict, Any, List, Optional
import os
import json
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
import subprocess

from svt_app.services.question_service import QuestionService
from svt_app.services.texte_a_trous_service import TexteATrousService
from svt_app.utils.logging_utils import conditional_log, log_if_enabled
from svt_app.controllers.settings_controller import load_settings
from svt_app.state import GameScores

# Create a Blueprint for the game routes
game_bp = Blueprint("game", __name__)

# Initialize the services
conditional_log("Initializing services")
question_service = QuestionService()
texte_a_trous_service = TexteATrousService(question_service)

@game_bp.route("/texte_a_trous")
def texte_a_trous() -> str:
    """
    Render the 'Texte à trous' game page.
    
    Returns:
        str: Rendered HTML template for the 'Texte à trous' game.
    """
    # Get question ID from request parameters
    question_id = request.args.get("question_id", None, type=int)
    
    # Get focused folder from request parameters
    focused_folder = request.args.get("focus", "")
    conditional_log("Texte à trous: received focus parameter: '{}'", focused_folder)
    
    # Get game data from service
    game_data = texte_a_trous_service.get_game_data(question_id, focused_folder)
    
    # Render template with game data
    return render_template("texte_a_trous.html", **game_data)


@game_bp.route("/relier_images")
def relier_images() -> str:
    """
    Render the 'Relier les images' game page.
    
    Returns:
        str: Rendered HTML template for the 'Relier les images' game.
    """
    questions = question_service.get_image_matching_questions()
    
    # Get the current question ID from the query parameters, default to 1
    question_id = request.args.get("question_id", 1, type=int)
    
    # Get the current question
    current_question = question_service.get_image_matching_question_by_id(question_id)
    
    # If the question doesn't exist, redirect to the first question
    if current_question is None and questions:
        return redirect(url_for("game.relier_images", question_id=questions[0].id))
    
    # If there are no questions, show an empty template
    if not questions:
        return render_template("relier_images.html", question=None, scores=GameScores.get_scores())
    
    # Combine correct and incorrect words and shuffle them
    all_words = [current_question.correct_word] + current_question.incorrect_words
    
    return render_template(
        "relier_images.html",
        question=current_question,
        words=all_words,
        question_id=question_id,
        total_questions=len(questions),
        scores=GameScores.get_scores()
    )


@game_bp.route("/check_answer", methods=["POST"])
def check_answer() -> Dict[str, Any]:
    """
    Check if the submitted answer is correct and update question statistics.
    
    Returns:
        Dict[str, Any]: JSON response with the result.
    """
    try:
        data = request.get_json()
        conditional_log("Received answer data: {}", data)
        
        if not data:
            conditional_log("No data provided in answer submission")
            return jsonify({"success": False, "message": "No data provided"})
        
        game_type = data.get("game_type")
        question_id = data.get("question_id")
        answer = data.get("answer")
        
        conditional_log("Processing answer - Game: {}, Question: {}, Answer: {}", 
                 game_type, question_id, answer)
        
        # Validate required fields
        if not all([game_type, question_id is not None, answer]):
            conditional_log("Missing required fields in answer submission")
            return jsonify({"success": False, "message": "Missing required fields"})
        
        # Ensure question_id is an integer
        try:
            question_id = int(question_id)
        except (TypeError, ValueError):
            conditional_log("Invalid question ID format: {}", question_id)
            return jsonify({"success": False, "message": "Invalid question ID"})
        
        # Check the answer based on the game type
        if game_type == "texte_a_trous":
            question = question_service.get_fill_in_blank_question_by_id(question_id)
            conditional_log("Retrieved question for checking: {}", question)
            
            if not question:
                conditional_log("Question not found: {}", question_id)
                return jsonify({"success": False, "message": "Question not found"})
            
            # Find the question file in all subdirectories
            base_dir = "assets/Data/fill_the_blanks"
            question_file = f"question{question_id:03d}.json"
            file_path = None
            
            # First try to find the file in the root directory
            root_path = os.path.join(base_dir, question_file)
            if os.path.exists(root_path):
                file_path = root_path
            else:
                # If not found in root, search in subdirectories
                for root, _, files in os.walk(base_dir):
                    if question_file in files:
                        file_path = os.path.join(root, question_file)
                        break
            
            if not file_path:
                conditional_log("Could not find file for question {}", question_id)
                return jsonify({"success": False, "message": "Question file not found"})
            
            is_correct = answer == question.correct_answer
            conditional_log("Answer is {}", "correct" if is_correct else "incorrect")
            
            try:
                # Load existing data
                with open(file_path, 'r', encoding='utf-8') as f:
                    question_data = json.load(f)
                
                # Update statistics
                stats = question_data.get('statistics', {'correct_answers': 0, 'wrong_answers': 0})
                if is_correct:
                    stats['correct_answers'] = stats.get('correct_answers', 0) + 1
                    GameScores.increment_score("texte_a_trous")
                    
                    # Load settings and check auto_validate
                    settings = load_settings()
                    # Only mark as completed when auto_validate is true
                    if settings.get('auto_validate', True):
                        question_data['completed'] = True
                        conditional_log("Question {} marked as completed", question_id)
                else:
                    stats['wrong_answers'] = stats.get('wrong_answers', 0) + 1
                
                question_data['statistics'] = stats
                
                # Save updated data
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(question_data, f, indent=4, ensure_ascii=False)
                
                conditional_log("Updated question data: {}", question_data)
                
                # Find the next available question ID
                active_questions = []
                conditional_log("Finding next available question after ID {}", question_id)
                
                # First, get all questions sorted by ID
                all_questions = sorted(question_service.get_fill_in_blank_questions(), key=lambda x: x.id)
                question_ids = [q.id for q in all_questions]
                conditional_log("All questions (sorted): {}", question_ids)
                
                # Then filter for active (non-completed) questions
                for q in all_questions:
                    q_file = os.path.join(base_dir, f"question{q.id:03d}.json")
                    if os.path.exists(q_file):
                        try:
                            with open(q_file, 'r', encoding='utf-8') as f:
                                q_data = json.load(f)
                                if not q_data.get('completed', False):
                                    active_questions.append(q.id)
                                    conditional_log("Found active question: {}", q.id)
                        except Exception as e:
                            conditional_log("Error reading question file {}: {}", q_file, str(e))
                            continue
                
                conditional_log("Active (non-completed) questions: {}", active_questions)
                
                # Find the next available question ID after the current one
                next_question_id = None
                
                if active_questions:
                    # Sort active questions to ensure proper order
                    active_questions.sort()
                    conditional_log("Sorted active questions: {}", active_questions)
                    
                    # Try to find the next question after current one
                    for q_id in active_questions:
                        if q_id > question_id:
                            next_question_id = q_id
                            conditional_log("Found next question ID: {}", next_question_id)
                            break
                    
                    # If no next question found, loop back to the first active question
                    if next_question_id is None:
                        # Make sure we don't return to the current question
                        remaining_questions = [q for q in active_questions if q != question_id]
                        if remaining_questions:
                            next_question_id = remaining_questions[0]
                            conditional_log("No next question found, looping back to first remaining question: {}", next_question_id)
                        else:
                            conditional_log("No other active questions available")
                else:
                    conditional_log("No active questions found")
                
                conditional_log("Final next_question_id: {}", next_question_id)
                
                # Create the response data
                response_data = {
                    "success": True,
                    "correct": is_correct,
                    "score": GameScores.get_score("texte_a_trous"),
                    "next_question_id": next_question_id
                }
                conditional_log("Sending response: {}", response_data)
                return jsonify(response_data)
                
            except Exception as e:
                conditional_log("Error processing question: {}", str(e))
                return jsonify({
                    "success": True,
                    "correct": is_correct,
                    "score": GameScores.get_score("texte_a_trous"),
                    "next_question_id": None,
                    "error": str(e)
                })
                
        elif game_type == "relier_images":
            question = question_service.get_image_matching_question_by_id(question_id)
            conditional_log("Image matching question: {}", question)
            if question and answer == question.correct_word:
                GameScores.increment_score("relier_images")
                return jsonify({"success": True, "correct": True, "score": GameScores.get_score("relier_images")})
            return jsonify({"success": True, "correct": False, "score": GameScores.get_score("relier_images")})
        
        conditional_log("Invalid game type")
        return jsonify({"success": False, "message": "Invalid game type"})
    
    except Exception as e:
        conditional_log("Error processing request: {}", str(e))
        return jsonify({"success": False, "message": "Une erreur est survenue lors de la validation"})


@game_bp.route("/reset_scores", methods=["POST"])
def reset_scores() -> Dict[str, Any]:
    """
    Reset the game scores.
    
    Sets all game scores to 0.
    
    Returns:
        Dict[str, Any]: JSON response indicating success.
    """
    GameScores.reset_scores()  # Use the correct method name
    
    conditional_log("Scores reset - texte_a_trous: {}, relier_images: {}", 
              GameScores.get_score("texte_a_trous"), GameScores.get_score("relier_images"))
    
    return jsonify({"success": True})


@game_bp.route("/create_question", methods=["GET"])
def create_question() -> str:
    """
    Render the question creation form.
    
    Returns:
        str: Rendered HTML template for creating a new question.
    """
    game_type = request.args.get('type', 'texte_a_trous')
    if game_type not in ['texte_a_trous', 'relier_images']:
        game_type = 'texte_a_trous'
    
    return render_template("create_question.html", game_type=game_type)


@game_bp.route("/save_question", methods=["POST"])
def save_question() -> Dict[str, Any]:
    """
    Save a new question (either fill-in-the-blank or image matching).
    
    Returns:
        Dict[str, Any]: JSON response indicating success or failure.
    """
    try:
        data = request.get_json()
        if not data or 'game_type' not in data:
            return jsonify({"success": False, "message": "No data or game type provided"})
        
        game_type = data['game_type']
        if game_type not in ['texte_a_trous', 'relier_images']:
            return jsonify({"success": False, "message": "Invalid game type"})
        
        # Validate required fields based on game type
        if game_type == 'texte_a_trous':
            required_fields = ["text", "options", "correct_answer"]
        else:  # relier_images
            required_fields = ["text", "correct_word", "incorrect_words", "image_path"]
        
        if not all(field in data for field in required_fields):
            return jsonify({"success": False, "message": "Missing required fields"})
        
        # Additional validation based on game type
        if game_type == 'texte_a_trous':
            if data["correct_answer"] not in data["options"]:
                return jsonify({"success": False, "message": "La réponse correcte doit correspondre exactement à l'une des options"})
        else:  # relier_images
            if not data["incorrect_words"] or not isinstance(data["incorrect_words"], list):
                return jsonify({"success": False, "message": "Les mots incorrects doivent être une liste non vide"})
        
        # Get the next question number
        base_dir = "assets/Data/fill_the_blanks" if game_type == "texte_a_trous" else "assets/Data/image_matching"
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        
        existing_questions = [f for f in os.listdir(base_dir) if f.startswith("question") and f.endswith(".json")]
        next_num = 1
        if existing_questions:
            nums = [int(q[8:11]) for q in existing_questions]
            next_num = max(nums) + 1
        
        # Format the question number with leading zeros
        question_num = f"{next_num:03d}"
        filename = f"question{question_num}.json"
        
        # Create the question data based on game type
        if game_type == 'texte_a_trous':
            question_data = {
                "text": data["text"],
                "options": data["options"],
                "correct_answer": data["correct_answer"]
            }
        else:  # relier_images
            question_data = {
                "text": data["text"],
                "correct_word": data["correct_word"],
                "incorrect_words": data["incorrect_words"],
                "image_path": data["image_path"]
            }
        
        # Save the question file
        filepath = os.path.join(base_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(question_data, f, ensure_ascii=False, indent=2)
        
        return jsonify({"success": True, "message": "Question créée avec succès"})
    
    except Exception as e:
        conditional_log("Error saving question: {}", str(e))
        return jsonify({"success": False, "message": "Une erreur est survenue lors de la sauvegarde de la question"})



@game_bp.route("/questions_tree")
def questions_tree() -> str:
    """
    Render the questions tree visualization page.
    
    Returns:
        str: Rendered HTML template for the questions tree.
    """
    # Reload questions to capture any newly created ones
    question_service.load_questions()
    
    # Get the game type from query parameters, default to texte_a_trous
    game_type = request.args.get('type', 'texte_a_trous')
    
    # Get the focused folder from query parameters
    focused_folder = request.args.get('focus', '')
    conditional_log("Received focus parameter: '{}'", focused_folder)
    
    # Validate game type
    if game_type not in ['texte_a_trous', 'relier_images']:
        game_type = 'texte_a_trous'
    
    def get_questions_in_directory(directory: str, relative_path: str = "") -> List[Dict[str, Any]]:
        """
        Recursively get all questions in a directory and its subdirectories.
        
        Args:
            directory: The absolute directory path
            relative_path: The relative path from the base questions directory
            
        Returns:
            List[Dict[str, Any]]: List of questions and folders
        """
        items: List[Dict[str, Any]] = []
        
        try:
            # Make sure directory exists
            if not os.path.exists(directory):
                conditional_log("Directory does not exist: {}", directory)
                return items
                
            # Get all items in the directory
            dir_contents = os.listdir(directory)
            conditional_log("Found {} items in directory {}", len(dir_contents), directory)
            
            for item in sorted(dir_contents):
                full_path = os.path.join(directory, item)
                rel_path = os.path.join(relative_path, item) if relative_path else item
                
                if os.path.isdir(full_path):
                    # If it's a directory, recursively get its contents
                    conditional_log("Found directory: {}", full_path)
                    subfolder_items = get_questions_in_directory(full_path, rel_path)
                    
                    # Add folder even if empty
                    folder_data = {
                        'type': 'folder',
                        'name': item,
                        'path': rel_path,
                        'children': subfolder_items
                    }
                    items.append(folder_data)
                    conditional_log("Added folder: {} with {} children", item, len(subfolder_items))
                    
                elif item.startswith("question") and item.endswith(".json"):
                    # If it's a question file, add it to the list
                    try:
                        with open(full_path, 'r', encoding='utf-8') as f:
                            question_data = json.load(f)
                            items.append({
                                'type': 'question',
                                'id': item[8:11],  # Extract number from filename
                                'text': question_data.get('text', 'No text available'),
                                'file': rel_path,
                                'completed': question_data.get('completed', False),
                                'statistics': question_data.get('statistics', {
                                    'correct_answers': 0,
                                    'wrong_answers': 0
                                })
                            })
                            conditional_log("Added question: {}", item)
                    except Exception as e:
                        conditional_log("Error reading question file {}: {}", full_path, str(e))
                        continue
        except Exception as e:
            conditional_log("Error reading directory {}: {}", directory, str(e))
            return []
        
        return items

    def get_questions_in_focused_folder(directory: str, focused_folder: str) -> List[Dict[str, Any]]:
        """
        Get questions only from a specific focused folder (no subfolders).
        
        Args:
            directory: The absolute base directory path
            focused_folder: The relative path of the folder to focus on
            
        Returns:
            List[Dict[str, Any]]: List of questions from the focused folder only
        """
        items: List[Dict[str, Any]] = []
        
        try:
            # Build the full path to the focused folder
            focused_path = os.path.join(directory, focused_folder) if focused_folder else directory
            
            # Make sure the focused directory exists
            if not os.path.exists(focused_path):
                conditional_log("Focused directory does not exist: {}", focused_path)
                return items
                
            # Get all items in the focused directory only
            dir_contents = os.listdir(focused_path)
            conditional_log("Found {} items in focused directory {}", len(dir_contents), focused_path)
            
            for item in sorted(dir_contents):
                full_path = os.path.join(focused_path, item)
                rel_path = os.path.join(focused_folder, item) if focused_folder else item
                
                if item.startswith("question") and item.endswith(".json"):
                    # If it's a question file, add it to the list
                    try:
                        with open(full_path, 'r', encoding='utf-8') as f:
                            question_data = json.load(f)
                            items.append({
                                'type': 'question',
                                'id': item[8:11],  # Extract number from filename
                                'text': question_data.get('text', 'No text available'),
                                'file': rel_path,
                                'completed': question_data.get('completed', False),
                                'statistics': question_data.get('statistics', {
                                    'correct_answers': 0,
                                    'wrong_answers': 0
                                })
                            })
                            conditional_log("Added focused question: {}", item)
                    except Exception as e:
                        conditional_log("Error reading question file {}: {}", full_path, str(e))
                        continue
                        
        except Exception as e:
            conditional_log("Error reading focused directory {}: {}", focused_path, str(e))
            return []
        
        return items
    
    # Set the base directory based on game type
    base_dir = "assets/Data/fill_the_blanks" if game_type == "texte_a_trous" else "assets/Data/image_matching"
    
    # Create the base directory if it doesn't exist
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
        conditional_log("Created directory: {}", base_dir)
    
    # Check if we have a focused folder
    if focused_folder:
        # Validate the focused folder path exists
        focused_path = os.path.join(base_dir, focused_folder)
        if not os.path.exists(focused_path) or not os.path.isdir(focused_path):
            conditional_log("Invalid focused folder: {}", focused_folder)
            focused_folder = ""  # Reset if invalid
        
    if focused_folder:
        # Get questions only from the focused folder
        conditional_log("Getting questions from focused folder: {}", focused_folder)
        tree_data = get_questions_in_focused_folder(base_dir, focused_folder)
        conditional_log("Found {} questions in focused folder", len(tree_data))
        conditional_log("Tree data items: {}", [item.get('file', item.get('name', 'unknown')) for item in tree_data])
    else:
        # Get all questions and folders starting from the base directory
        conditional_log("Scanning directory tree starting from: {}", base_dir)
        tree_data = get_questions_in_directory(base_dir)
        conditional_log("Found {} top-level items in tree", len(tree_data))
    
    return render_template("questions_tree.html", tree_data=tree_data, game_type=game_type, focused_folder=focused_folder)


@game_bp.route("/toggle_question_completion", methods=["POST"])
def toggle_question_completion() -> Dict[str, Any]:
    """
    Toggle the completion status of a question.
    
    Returns:
        Dict[str, Any]: JSON response indicating success or failure.
    """
    try:
        data = request.get_json()
        if not data or 'file' not in data:
            return jsonify({"success": False, "message": "No file specified"})
        
        filename = data['file']
        # Only validate the filename part, not the full path
        if not os.path.basename(filename).startswith('question') or not filename.endswith('.json'):
            return jsonify({"success": False, "message": "Invalid file name"})
        
        file_path = os.path.join('assets/Data/fill_the_blanks', filename)
        
        # Check if file exists
        if not os.path.exists(file_path):
            return jsonify({"success": False, "message": "File not found"})
        
        # Read current question data
        with open(file_path, 'r', encoding='utf-8') as f:
            question_data = json.load(f)
        
        # Toggle completion status
        question_data['completed'] = not question_data.get('completed', False)
        
        # Save updated question data
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(question_data, f, ensure_ascii=False, indent=2)
        
        return jsonify({
            "success": True, 
            "completed": question_data['completed'],
            "message": "Question marquée comme " + ("terminée" if question_data['completed'] else "non terminée")
        })
    
    except Exception as e:
        conditional_log("Error toggling question completion: {}", str(e))
        return jsonify({"success": False, "message": "Une erreur est survenue lors de la mise à jour de la question"})


@game_bp.route("/delete_question", methods=["POST"])
def delete_question() -> Dict[str, Any]:
    """
    Delete a question file.
    
    Returns:
        Dict[str, Any]: JSON response indicating success or failure.
    """
    try:
        data = request.get_json()
        if not data or 'file' not in data:
            return jsonify({"success": False, "message": "No file specified"})
        
        filename = data['file']
        # Only validate the filename part, not the full path
        if not os.path.basename(filename).startswith('question') or not filename.endswith('.json'):
            return jsonify({"success": False, "message": "Invalid file name"})
        
        file_path = os.path.join('assets/Data/fill_the_blanks', filename)
        
        # Check if file exists
        if not os.path.exists(file_path):
            return jsonify({"success": False, "message": "File not found"})
        
        # Delete the file
        os.remove(file_path)
        
        return jsonify({"success": True, "message": "Question supprimée avec succès"})
    
    except Exception as e:
        conditional_log("Error deleting question: {}", str(e))
        return jsonify({"success": False, "message": "Une erreur est survenue lors de la suppression de la question"})


@game_bp.route("/create_folder", methods=["POST"])
def create_folder() -> Dict[str, Any]:
    """
    Create a new folder in the questions directory.
    
    Returns:
        Dict[str, Any]: JSON response indicating success or failure.
    """
    try:
        data = request.get_json()
        if not data or 'name' not in data or 'parent_path' not in data:
            return jsonify({"success": False, "message": "Missing folder name or parent path"})
        
        folder_name = data['name'].strip()
        parent_path = data['parent_path'].strip()
        
        # Validate folder name
        if not folder_name or '/' in folder_name or '\\' in folder_name:
            return jsonify({"success": False, "message": "Invalid folder name"})
        
        # Construct the full path
        base_dir = "assets/Data/fill_the_blanks"
        new_folder_path = os.path.join(base_dir, parent_path, folder_name)
        
        # Check if folder already exists
        if os.path.exists(new_folder_path):
            return jsonify({"success": False, "message": "Un dossier avec ce nom existe déjà"})
        
        # Create the folder
        os.makedirs(new_folder_path)
        
        return jsonify({
            "success": True,
            "message": "Dossier créé avec succès",
            "folder": {
                "name": folder_name,
                "path": os.path.join(parent_path, folder_name) if parent_path else folder_name
            }
        })
    
    except Exception as e:
        conditional_log("Error creating folder: {}", str(e))
        return jsonify({"success": False, "message": "Une erreur est survenue lors de la création du dossier"})


@game_bp.route("/rename_folder", methods=["POST"])
def rename_folder() -> Dict[str, Any]:
    """
    Rename an existing folder.
    
    Returns:
        Dict[str, Any]: JSON response indicating success or failure.
    """
    try:
        data = request.get_json()
        if not data or 'old_path' not in data or 'new_name' not in data:
            return jsonify({"success": False, "message": "Missing required fields"})
        
        old_path = data['old_path'].strip()
        new_name = data['new_name'].strip()
        
        # Validate new name
        if not new_name or '/' in new_name or '\\' in new_name:
            return jsonify({"success": False, "message": "Invalid folder name"})
        
        # Construct paths
        base_dir = "assets/Data/fill_the_blanks"
        old_full_path = os.path.join(base_dir, old_path)
        new_full_path = os.path.join(base_dir, os.path.dirname(old_path), new_name)
        
        # Check if source exists and destination doesn't
        if not os.path.exists(old_full_path):
            return jsonify({"success": False, "message": "Folder not found"})
        if os.path.exists(new_full_path):
            return jsonify({"success": False, "message": "Un dossier avec ce nom existe déjà"})
        
        # Rename the folder
        os.rename(old_full_path, new_full_path)
        
        return jsonify({
            "success": True,
            "message": "Dossier renommé avec succès",
            "new_path": os.path.join(os.path.dirname(old_path), new_name)
        })
    
    except Exception as e:
        conditional_log("Error renaming folder: {}", str(e))
        return jsonify({"success": False, "message": "Une erreur est survenue lors du renommage du dossier"})


@game_bp.route("/delete_folder", methods=["POST"])
def delete_folder() -> Dict[str, Any]:
    """
    Delete a folder and all its contents.
    
    Returns:
        Dict[str, Any]: JSON response indicating success or failure.
    """
    try:
        data = request.get_json()
        if not data or 'path' not in data:
            return jsonify({"success": False, "message": "Missing folder path"})
        
        folder_path = data['path'].strip()
        
        # Construct full path
        base_dir = "assets/Data/fill_the_blanks"
        full_path = os.path.join(base_dir, folder_path)
        
        # Check if folder exists and is a directory
        if not os.path.exists(full_path) or not os.path.isdir(full_path):
            return jsonify({"success": False, "message": "Folder not found"})
        
        # Delete the folder and all its contents
        import shutil
        shutil.rmtree(full_path)
        
        return jsonify({
            "success": True,
            "message": "Dossier supprimé avec succès"
        })
    
    except Exception as e:
        conditional_log("Error deleting folder: {}", str(e))
        return jsonify({"success": False, "message": "Une erreur est survenue lors de la suppression du dossier"})


@game_bp.route("/move_items", methods=["POST"])
@log_if_enabled()
def move_items() -> Dict[str, Any]:
    """
    Move questions or folders to a new location.
    
    Returns:
        Dict[str, Any]: JSON response indicating success or failure.
    """
    try:
        conditional_log("Move items request received")
        data = request.get_json()
        conditional_log("Request data: {}", data)
        
        if not data or 'items' not in data or 'target_folder' not in data or 'types' not in data:
            conditional_log("Missing required fields in request data")
            return jsonify({"success": False, "message": "Missing required fields"})
        
        items = data['items']  # List of file/folder paths to move
        types = data['types']  # Dictionary mapping paths to their types (folder/question)
        target_folder = data['target_folder'].strip()  # Target folder path
        conditional_log("Moving items: {} with types {} to target folder: '{}'", items, types, target_folder)
        
        base_dir = "assets/Data/fill_the_blanks"
        conditional_log("Base directory: {}", base_dir)
        
        # Handle root directory case
        target_path = base_dir if target_folder == "" else os.path.join(base_dir, target_folder)
        conditional_log("Resolved target path: {}", target_path)
        
        # Create target directory if it doesn't exist
        os.makedirs(target_path, exist_ok=True)
        conditional_log("Target directory ensured: {}", target_path)
        
        moved_items = []
        for item_path in items:
            try:
                item_type = types.get(item_path)
                if not item_type:
                    conditional_log("No type information for item: {}", item_path)
                    continue
                    
                source_path = os.path.join(base_dir, item_path)
                conditional_log("Processing {} - source path: {}", item_type, source_path)
                
                if not os.path.exists(source_path):
                    conditional_log("Source path does not exist: {}", source_path)
                    continue
                
                # Get the base name of the item
                item_name = os.path.basename(item_path)
                new_path = os.path.join(target_path, item_name)
                conditional_log("Target path for {}: {}", item_type, new_path)
                
                # Skip if source and target are the same
                if os.path.abspath(source_path) == os.path.abspath(new_path):
                    conditional_log("Source and target paths are the same, skipping: {}", source_path)
                    continue
                
                # For folders, check if we're trying to move a folder into itself
                if item_type == 'folder' and new_path.startswith(source_path):
                    conditional_log("Cannot move folder into itself: {} -> {}", source_path, new_path)
                    continue
                
                # Check if an item with the same name already exists in target
                if os.path.exists(new_path):
                    # Generate a unique name by appending a number
                    base_name = os.path.splitext(item_name)[0]
                    ext = os.path.splitext(item_name)[1] if item_type == 'question' else ''
                    counter = 1
                    while os.path.exists(new_path):
                        new_name = f"{base_name}_{counter}{ext}"
                        new_path = os.path.join(target_path, new_name)
                        counter += 1
                    conditional_log("Generated unique path for existing {}: {}", item_type, new_path)
                
                # Move the item
                import shutil
                conditional_log("Attempting to move {} to {}", source_path, new_path)
                shutil.move(source_path, new_path)
                moved_items.append(item_path)
                conditional_log("Successfully moved {} to {}", source_path, new_path)
                
            except Exception as e:
                conditional_log("Error moving item {}: {}", item_path, str(e), level="ERROR")
                continue
        
        conditional_log("Move operation completed. Moved items: {}", moved_items)
        
        if not moved_items:
            conditional_log("No items were successfully moved")
            return jsonify({
                "success": False,
                "message": "Aucun élément n'a pu être déplacé"
            })
        
        response_data = {
            "success": True,
            "message": f"{len(moved_items)} élément(s) déplacé(s) avec succès",
            "moved_items": moved_items
        }
        conditional_log("Sending response: {}", response_data)
        return jsonify(response_data)
    
    except Exception as e:
        conditional_log("Error moving items: {}", str(e), level="ERROR")
        return jsonify({"success": False, "message": "Une erreur est survenue lors du déplacement des éléments"})


@game_bp.route('/open_folder', methods=['POST'])
def open_folder():
    """Open a folder in the system's file explorer."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'Invalid JSON data'}), 400
            
        folder_path = data.get('path', '')
        
        # Get the base directory (where the questions are stored)
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'assets', 'Data', 'fill_the_blanks'))
        
        # Join with the requested folder path
        abs_path = os.path.abspath(os.path.join(base_dir, folder_path))
        
        # Security check - make sure the path is within the base directory
        if not abs_path.startswith(base_dir):
            return jsonify({'success': False, 'message': 'Invalid folder path'}), 403
            
        # Check if the folder exists
        if not os.path.exists(abs_path):
            return jsonify({'success': False, 'message': 'Folder not found'}), 404
            
        if os.name == 'nt':  # Windows
            os.startfile(abs_path)
        elif os.name == 'posix':  # macOS and Linux
            if os.path.exists('/usr/bin/xdg-open'):  # Linux
                subprocess.run(['xdg-open', abs_path])
            else:  # macOS
                subprocess.run(['open', abs_path])
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500 