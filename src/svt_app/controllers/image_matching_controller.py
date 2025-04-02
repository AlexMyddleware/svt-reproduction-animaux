"""Image matching game controller module for Révijouer application."""

from typing import List
from flask import Blueprint, render_template, request, redirect, url_for

from svt_app.services.question_service import QuestionService
from svt_app.state import GameScores

# Create a Blueprint for the image matching routes
image_matching_bp = Blueprint("image_matching", __name__)

# Initialize the question service
question_service = QuestionService()

@image_matching_bp.route("/relier_images")
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
        return redirect(url_for("image_matching.relier_images", question_id=questions[0].id))
    
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