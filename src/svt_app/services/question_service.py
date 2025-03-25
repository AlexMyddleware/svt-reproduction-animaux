"""Question service module for SVT Reproduction Animaux application."""

import json
import os
import sys
from typing import List, Dict, Any, Optional
from pathlib import Path

from svt_app.models.question import FillInTheBlankQuestion, ImageMatchingQuestion


class QuestionService:
    """
    Service for loading and managing questions.
    
    This service handles loading questions from JSON files and provides
    methods to access questions for different game types.
    """
    
    def __init__(self) -> None:
        """Initialize the QuestionService."""
        # Get the base path - handles both development and PyInstaller executable
        if getattr(sys, 'frozen', False):
            # Running in PyInstaller bundle
            self.base_path = os.path.join(sys._MEIPASS)
        else:
            # Running in normal Python environment
            self.base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        
        # Initialize paths relative to base_path
        self.fill_blanks_path = os.path.join(self.base_path, "assets", "Data", "fill_the_blanks")
        self.image_matching_path = os.path.join(self.base_path, "assets", "Data", "image_matching")
        
        self.fill_in_blank_questions: List[FillInTheBlankQuestion] = []
        self.image_matching_questions: List[ImageMatchingQuestion] = []
        self.load_questions()
    
    def load_questions(self) -> None:
        """
        Load questions from JSON files.
        
        This method loads both fill-in-the-blank and image matching questions
        from their respective JSON files.
        """
        self._load_fill_in_blank_questions()
        self._load_image_matching_questions()
    
    def _load_fill_in_blank_questions(self) -> None:
        """
        Load fill-in-the-blank questions from JSON files.
        
        This is a private method that loads fill-in-the-blank questions
        from the assets/Data/fill_the_blanks directory.
        """
        if not os.path.exists(self.fill_blanks_path):
            return
        
        for file_path in Path(self.fill_blanks_path).glob("*.json"):
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    
                    question_id = int(file_path.stem.replace("question", ""))
                    
                    question = FillInTheBlankQuestion(
                        id=question_id,
                        text=data.get("text", ""),
                        options=data.get("options", []),
                        correct_answer=data.get("correct_answer", "")
                    )
                    
                    self.fill_in_blank_questions.append(question)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading question from {file_path}: {e}")
    
    def _load_image_matching_questions(self) -> None:
        """
        Load image matching questions from JSON files.
        
        This is a private method that loads image matching questions
        from the assets/Data/image_interaction directory.
        """
        if not os.path.exists(self.image_matching_path):
            return
        
        for file_path in Path(self.image_matching_path).glob("*.json"):
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    
                    question_id = int(file_path.stem.replace("question", ""))
                    
                    question = ImageMatchingQuestion(
                        id=question_id,
                        image_path=data.get("image", ""),
                        correct_word=data.get("words", {}).get("correct", ""),
                        incorrect_words=data.get("words", {}).get("incorrect", [])
                    )
                    
                    self.image_matching_questions.append(question)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading question from {file_path}: {e}")
    
    def get_fill_in_blank_questions(self) -> List[FillInTheBlankQuestion]:
        """
        Get all fill-in-the-blank questions.
        
        Returns:
            List[FillInTheBlankQuestion]: List of all fill-in-the-blank questions.
        """
        return self.fill_in_blank_questions
    
    def get_image_matching_questions(self) -> List[ImageMatchingQuestion]:
        """
        Get all image matching questions.
        
        Returns:
            List[ImageMatchingQuestion]: List of all image matching questions.
        """
        return self.image_matching_questions
    
    def get_fill_in_blank_question_by_id(self, question_id: int) -> Optional[FillInTheBlankQuestion]:
        """
        Get a fill-in-the-blank question by its ID.
        
        Args:
            question_id (int): The ID of the question to retrieve.
            
        Returns:
            Optional[FillInTheBlankQuestion]: The question with the given ID, or None if not found.
        """
        for question in self.fill_in_blank_questions:
            if question.id == question_id:
                return question
        return None
    
    def get_image_matching_question_by_id(self, question_id: int) -> Optional[ImageMatchingQuestion]:
        """
        Get an image matching question by its ID.
        
        Args:
            question_id (int): The ID of the question to retrieve.
            
        Returns:
            Optional[ImageMatchingQuestion]: The question with the given ID, or None if not found.
        """
        for question in self.image_matching_questions:
            if question.id == question_id:
                return question
        return None 