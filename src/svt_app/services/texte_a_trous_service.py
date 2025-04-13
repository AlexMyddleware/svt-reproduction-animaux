"""Service module for handling Texte à Trous game logic."""

from typing import List, Optional, Dict, Any
import os
import json
from svt_app.services.question_service import QuestionService
from svt_app.utils.logging_utils import conditional_log
from svt_app.state import GameScores

class TexteATrousService:
    """Service class for handling Texte à Trous game logic."""
    
    def __init__(self, question_service: QuestionService):
        """
        Initialize the TexteATrousService.
        
        Args:
            question_service: The question service instance to use.
        """
        self.question_service = question_service

    def get_active_questions(self) -> List[Any]:
        """
        Get all active (non-completed) questions for the Texte à Trous game.
        
        Returns:
            List[Any]: List of active questions.
        """
        conditional_log("Loading fill in the blank questions")
        # Reload questions to capture any newly created ones
        self.question_service.load_questions()
        questions = self.question_service.get_fill_in_blank_questions()
        
        # Filter out completed questions
        active_questions = []
        for question in questions:
            # Search for the question file in all subdirectories
            base_dir = "assets/Data/fill_the_blanks"
            question_file = f"question{question.id:03d}.json"
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
            
            if file_path:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        question_data = json.load(f)
                        if not question_data.get('completed', False):
                            active_questions.append(question)
                            conditional_log("Found active question {} in {}", question.id, file_path)
                except Exception as e:
                    conditional_log("Error reading question file {}: {}", file_path, str(e))
                    continue
            else:
                conditional_log("Warning: Could not find file for question {}", question.id)
        
        conditional_log("Found {} active questions", len(active_questions))
        return active_questions

    def get_current_question(self, question_id: Optional[int], active_questions: List[Any]) -> tuple[Optional[Any], Optional[int]]:
        """
        Get the current question based on the question ID and active questions.
        
        Args:
            question_id: The requested question ID, if any.
            active_questions: List of active questions.
            
        Returns:
            tuple[Optional[Any], Optional[int]]: A tuple containing the current question and its ID.
        """
        # If no active questions, return None
        if not active_questions:
            conditional_log("No active questions found")
            return None, None
        
        # Get the current question ID from the query parameters, default to first active question
        conditional_log("Requested question ID: {}", question_id)
        
        # If no question_id specified or the requested question is not in active questions,
        # use the first active question
        current_question = None
        if question_id is not None:
            # Try to find the requested question
            for q in active_questions:
                if q.id == question_id:
                    current_question = q
                    break
        
        # If no current question (either not specified or not found), use first active
        if current_question is None and active_questions:
            current_question = active_questions[0]
            question_id = current_question.id
        
        conditional_log("Selected question ID: {}, Question: {}", 
                question_id, 
                current_question.text if current_question else "None")
        
        return current_question, question_id

    def get_game_data(self, question_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Get all necessary data for rendering the Texte à Trous game.
        
        Args:
            question_id: Optional question ID to load.
            
        Returns:
            Dict[str, Any]: Dictionary containing all necessary game data.
        """
        active_questions = self.get_active_questions()
        current_question, question_id = self.get_current_question(question_id, active_questions)
        
        return {
            "question": current_question,
            "question_id": question_id,
            "total_questions": len(active_questions),
            "scores": GameScores.get_scores()
        } 