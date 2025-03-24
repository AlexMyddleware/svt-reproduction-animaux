"""Game controller module for SVT Reproduction Animaux application."""

from typing import Dict, Any, List, Optional
import os
import json
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session

from svt_app.services.question_service import QuestionService

# Create a Blueprint for the game routes
game_bp = Blueprint("game", __name__)

# Initialize the question service
question_service = QuestionService()

# Global scores dictionary
scores: Dict[str, int] = {
    "texte_a_trous": 0,
    "relier_images": 0
}


@game_bp.route("/texte_a_trous")
def texte_a_trous() -> str:
    """
    Render the 'Texte à trous' game page.
    
    Returns:
        str: Rendered HTML template for the 'Texte à trous' game.
    """
    questions = question_service.get_fill_in_blank_questions()
    
    # Filter out completed questions
    active_questions = []
    for question in questions:
        file_path = os.path.join("assets/Data/fill_the_blanks", f"question{question.id:03d}.json")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                question_data = json.load(f)
                if not question_data.get('completed', False):
                    active_questions.append(question)
        except Exception as e:
            print(f"Error reading question file: {e}")
            continue
    
    # If no active questions, show empty template
    if not active_questions:
        return render_template("texte_a_trous.html", question=None, scores=scores)
    
    # Get the current question ID from the query parameters, default to 1
    question_id = request.args.get("question_id", 1, type=int)
    
    # Get the current question
    current_question = None
    for q in active_questions:
        if q.id == question_id:
            current_question = q
            break
    
    # If the question doesn't exist or is completed, redirect to the first active question
    if current_question is None and active_questions:
        return redirect(url_for("game.texte_a_trous", question_id=active_questions[0].id))
    
    return render_template(
        "texte_a_trous.html",
        question=current_question,
        question_id=question_id,
        total_questions=len(active_questions),
        scores=scores
    )


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
        return render_template("relier_images.html", question=None, scores=scores)
    
    # Combine correct and incorrect words and shuffle them
    all_words = [current_question.correct_word] + current_question.incorrect_words
    
    return render_template(
        "relier_images.html",
        question=current_question,
        words=all_words,
        question_id=question_id,
        total_questions=len(questions),
        scores=scores
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
        print("Received data:", data)  # Debug log
        
        if not data:
            print("No data provided")  # Debug log
            return jsonify({"success": False, "message": "No data provided"})
        
        game_type = data.get("game_type")
        question_id = data.get("question_id")
        answer = data.get("answer")
        
        print(f"Game type: {game_type}, Question ID: {question_id}, Answer: {answer}")  # Debug log
        
        # Validate required fields
        if not all([game_type, question_id is not None, answer]):
            print("Missing required fields")  # Debug log
            return jsonify({"success": False, "message": "Missing required fields"})
        
        # Ensure question_id is an integer
        try:
            question_id = int(question_id)
        except (TypeError, ValueError):
            print(f"Invalid question ID: {question_id}")  # Debug log
            return jsonify({"success": False, "message": "Invalid question ID"})
        
        # Check the answer based on the game type
        if game_type == "texte_a_trous":
            question = question_service.get_fill_in_blank_question_by_id(question_id)
            print("Fill in blank question:", question)  # Debug log
            
            # Find the question file
            file_path = os.path.join("assets/Data/fill_the_blanks", f"question{question_id:03d}.json")
            
            # If the file doesn't exist in root, search in subfolders
            if not os.path.exists(file_path):
                base_dir = "assets/Data/fill_the_blanks"
                for root, _, files in os.walk(base_dir):
                    for file in files:
                        if file == f"question{question_id:03d}.json":
                            file_path = os.path.join(root, file)
                            break
            
            # Update statistics in the question file
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    question_data = json.load(f)
                
                # Initialize statistics if they don't exist
                if 'statistics' not in question_data:
                    question_data['statistics'] = {'correct_answers': 0, 'wrong_answers': 0}
                
                # Update the appropriate counter
                is_correct = question and answer == question.correct_answer
                if is_correct:
                    question_data['statistics']['correct_answers'] += 1
                    scores["texte_a_trous"] += 1
                else:
                    question_data['statistics']['wrong_answers'] += 1
                
                # Save the updated statistics
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(question_data, f, ensure_ascii=False, indent=2)
                
                return jsonify({
                    "success": True, 
                    "correct": is_correct, 
                    "score": scores["texte_a_trous"],
                    "statistics": question_data['statistics']
                })
                
            except Exception as e:
                print(f"Error updating question statistics: {e}")
                # Continue with normal response if statistics update fails
                return jsonify({
                    "success": True,
                    "correct": question and answer == question.correct_answer,
                    "score": scores["texte_a_trous"]
                })
            
        elif game_type == "relier_images":
            question = question_service.get_image_matching_question_by_id(question_id)
            print("Image matching question:", question)  # Debug log
            if question and answer == question.correct_word:
                scores["relier_images"] += 1
                return jsonify({"success": True, "correct": True, "score": scores["relier_images"]})
            return jsonify({"success": True, "correct": False, "score": scores["relier_images"]})
        
        print("Invalid game type")  # Debug log
        return jsonify({"success": False, "message": "Invalid game type"})
    
    except Exception as e:
        print(f"Error processing request: {e}")  # Debug log
        return jsonify({"success": False, "message": "Une erreur est survenue lors de la validation"})


@game_bp.route("/reset_scores")
def reset_scores() -> str:
    """
    Reset all game scores to zero.
    
    Returns:
        str: Redirect to the main menu.
    """
    global scores
    scores = {
        "texte_a_trous": 0,
        "relier_images": 0
    }
    return redirect(url_for("index"))


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
        print(f"Error saving question: {e}")
        return jsonify({"success": False, "message": "Une erreur est survenue lors de la sauvegarde de la question"})


@game_bp.route("/questions_tree")
def questions_tree() -> str:
    """
    Render the questions tree visualization page.
    
    Returns:
        str: Rendered HTML template for the questions tree.
    """
    # Get the game type from query parameters, default to texte_a_trous
    game_type = request.args.get('type', 'texte_a_trous')
    
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
            # Get all items in the directory
            for item in sorted(os.listdir(directory)):
                full_path = os.path.join(directory, item)
                rel_path = os.path.join(relative_path, item) if relative_path else item
                
                if os.path.isdir(full_path):
                    # If it's a directory, recursively get its contents
                    subfolder_items = get_questions_in_directory(full_path, rel_path)
                    if subfolder_items:  # Only add non-empty folders
                        folder_data = {
                            'type': 'folder',
                            'name': item,
                            'path': rel_path,
                            'children': subfolder_items
                        }
                        items.append(folder_data)
                elif item.startswith("question") and item.endswith(".json"):
                    # If it's a question file, add it to the list
                    try:
                        with open(full_path, 'r', encoding='utf-8') as f:
                            question_data = json.load(f)
                            items.append({
                                'type': 'question',
                                'id': item[8:11],  # Extract number from filename
                                'text': question_data['text'],
                                'file': rel_path,
                                'completed': question_data.get('completed', False),
                                'statistics': question_data.get('statistics', {
                                    'correct_answers': 0,
                                    'wrong_answers': 0
                                })
                            })
                    except Exception as e:
                        print(f"Error reading question file {full_path}: {e}")
                        continue
        except Exception as e:
            print(f"Error reading directory {directory}: {e}")
            return []
        
        return items
    
    # Set the base directory based on game type
    base_dir = "assets/Data/fill_the_blanks" if game_type == "texte_a_trous" else "assets/Data/image_matching"
    
    # Create the base directory if it doesn't exist
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    
    # Get all questions and folders starting from the base directory
    tree_data = get_questions_in_directory(base_dir)
    
    return render_template("questions_tree.html", tree_data=tree_data, game_type=game_type)


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
        print(f"Error toggling question completion: {e}")
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
        print(f"Error deleting question: {e}")
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
        print(f"Error creating folder: {e}")
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
        print(f"Error renaming folder: {e}")
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
        print(f"Error deleting folder: {e}")
        return jsonify({"success": False, "message": "Une erreur est survenue lors de la suppression du dossier"})


@game_bp.route("/move_items", methods=["POST"])
def move_items() -> Dict[str, Any]:
    """
    Move questions or folders to a new location.
    
    Returns:
        Dict[str, Any]: JSON response indicating success or failure.
    """
    try:
        data = request.get_json()
        if not data or 'items' not in data or 'target_folder' not in data:
            return jsonify({"success": False, "message": "Missing required fields"})
        
        items = data['items']  # List of file/folder paths to move
        target_folder = data['target_folder'].strip()  # Target folder path
        
        base_dir = "assets/Data/fill_the_blanks"
        target_path = os.path.join(base_dir, target_folder)
        
        # Check if target folder exists
        if not os.path.exists(target_path) or not os.path.isdir(target_path):
            return jsonify({"success": False, "message": "Target folder not found"})
        
        moved_items = []
        for item_path in items:
            try:
                source_path = os.path.join(base_dir, item_path)
                if not os.path.exists(source_path):
                    continue
                
                # Get the base name of the item
                item_name = os.path.basename(item_path)
                new_path = os.path.join(target_path, item_name)
                
                # Check if an item with the same name already exists in target
                if os.path.exists(new_path):
                    continue
                
                # Move the item
                import shutil
                shutil.move(source_path, new_path)
                moved_items.append(item_path)
                
            except Exception as e:
                print(f"Error moving item {item_path}: {e}")
                continue
        
        return jsonify({
            "success": True,
            "message": f"{len(moved_items)} élément(s) déplacé(s) avec succès",
            "moved_items": moved_items
        })
    
    except Exception as e:
        print(f"Error moving items: {e}")
        return jsonify({"success": False, "message": "Une erreur est survenue lors du déplacement des éléments"}) 