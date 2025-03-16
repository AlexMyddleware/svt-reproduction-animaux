"""Game controller module for SVT Reproduction Animaux application."""

from typing import Dict, Any, List, Optional
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session

from src.svt_app.services.question_service import QuestionService

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
    
    # Get the current question ID from the query parameters, default to 1
    question_id = request.args.get("question_id", 1, type=int)
    
    # Get the current question
    current_question = question_service.get_fill_in_blank_question_by_id(question_id)
    
    # If the question doesn't exist, redirect to the first question
    if current_question is None and questions:
        return redirect(url_for("game.texte_a_trous", question_id=questions[0].id))
    
    # If there are no questions, show an empty template
    if not questions:
        return render_template("texte_a_trous.html", question=None, scores=scores)
    
    return render_template(
        "texte_a_trous.html",
        question=current_question,
        question_id=question_id,
        total_questions=len(questions),
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
    Check if the submitted answer is correct.
    
    Returns:
        Dict[str, Any]: JSON response with the result.
    """
    data = request.get_json()
    
    if not data:
        return jsonify({"success": False, "message": "No data provided"})
    
    game_type = data.get("game_type")
    question_id = data.get("question_id")
    answer = data.get("answer")
    
    if not all([game_type, question_id, answer]):
        return jsonify({"success": False, "message": "Missing required fields"})
    
    # Check the answer based on the game type
    if game_type == "texte_a_trous":
        question = question_service.get_fill_in_blank_question_by_id(question_id)
        if question and answer == question.correct_answer:
            scores["texte_a_trous"] += 1
            return jsonify({"success": True, "correct": True, "score": scores["texte_a_trous"]})
        return jsonify({"success": True, "correct": False, "score": scores["texte_a_trous"]})
    
    elif game_type == "relier_images":
        question = question_service.get_image_matching_question_by_id(question_id)
        if question and answer == question.correct_word:
            scores["relier_images"] += 1
            return jsonify({"success": True, "correct": True, "score": scores["relier_images"]})
        return jsonify({"success": True, "correct": False, "score": scores["relier_images"]})
    
    return jsonify({"success": False, "message": "Invalid game type"})


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