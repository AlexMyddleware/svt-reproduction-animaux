"""Question service module for SVT Reproduction Animaux application."""

import json
import os
import sys
from typing import List, Dict, Any, Optional
from pathlib import Path

from svt_app.models.question import FillInTheBlankQuestion, ImageMatchingQuestion
from svt_app.utils.debug import debug_log


class QuestionService:
    """
    Service for loading and managing questions.
    
    This service handles loading questions from JSON files and provides
    methods to access questions for different game types.
    """
    
    def __init__(self) -> None:
        """Initialize the QuestionService."""
        debug_log("Initializing QuestionService")
        
        # Get the base path - handles both development and PyInstaller executable
        if getattr(sys, 'frozen', False):
            # Running in PyInstaller bundle
            self.base_path = os.path.join(sys._MEIPASS)
            debug_log("Running in PyInstaller bundle, base path: {}", self.base_path)
        else:
            # Running in normal Python environment
            self.base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            debug_log("Running in development environment, base path: {}", self.base_path)
        
        # Initialize paths relative to base_path
        self.fill_blanks_path = os.path.join(self.base_path, "assets", "Data", "fill_the_blanks")
        self.image_matching_path = os.path.join(self.base_path, "assets", "Data", "image_matching")
        
        debug_log("Fill in blanks path: {}", self.fill_blanks_path)
        debug_log("Image matching path: {}", self.image_matching_path)
        
        self.fill_in_blank_questions: List[FillInTheBlankQuestion] = []
        self.image_matching_questions: List[ImageMatchingQuestion] = []
        self.load_questions()
    
    def load_questions(self) -> None:
        """
        Load questions from JSON files.
        
        This method loads both fill-in-the-blank and image matching questions
        from their respective JSON files.
        """
        debug_log("Loading all questions")
        self._load_fill_in_blank_questions()
        self._load_image_matching_questions()
    
    def _load_fill_in_blank_questions(self) -> None:
        """Load fill-in-the-blank questions from JSON files."""
        debug_log("Loading fill-in-the-blank questions")
        self.fill_in_blank_questions = []
        
        try:
            # Walk through the directory and its subdirectories
            for root, _, files in os.walk(self.fill_blanks_path):
                for file in files:
                    if file.startswith("question") and file.endswith(".json"):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                                debug_log("Loaded JSON data from {}: {}", file_path, data)
                                
                                # Extract question ID from filename (e.g., "question001.json" -> 1)
                                question_id = int(file[8:11])
                                
                                question = FillInTheBlankQuestion(
                                    id=question_id,
                                    text=data.get('text', ''),
                                    options=data.get('options', []),
                                    correct_answer=data.get('correct_answer', '')
                                )
                                self.fill_in_blank_questions.append(question)
                                debug_log("Loaded fill-in-blank question {}: {}", question.id, question.text)
                        except Exception as e:
                            debug_log("Error loading fill-in-blank question {}: {}", file_path, str(e))
                            continue
        except Exception as e:
            debug_log("Error walking fill-in-blank questions directory: {}", str(e))
        
        debug_log("Loaded {} fill-in-blank questions", len(self.fill_in_blank_questions))
    
    def _load_image_matching_questions(self) -> None:
        """Load image matching questions from JSON files."""
        debug_log("Loading image matching questions")
        self.image_matching_questions = []
        
        try:
            # Walk through the directory and its subdirectories
            for root, _, files in os.walk(self.image_matching_path):
                for file in files:
                    if file.startswith("question") and file.endswith(".json"):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                                debug_log("Loaded JSON data from {}: {}", file_path, data)
                                
                                # Extract question ID from filename
                                question_id = int(file[8:11])
                                
                                # Get words data
                                words_data = data.get('words', {})
                                
                                question = ImageMatchingQuestion(
                                    id=question_id,
                                    image_path=data.get('image', ''),
                                    correct_word=words_data.get('correct', ''),
                                    incorrect_words=words_data.get('incorrect', [])
                                )
                                self.image_matching_questions.append(question)
                                debug_log("Loaded image matching question {}: {}", question.id, question.image_path)
                        except Exception as e:
                            debug_log("Error loading image matching question {}: {}", file_path, str(e))
                            continue
        except Exception as e:
            debug_log("Error walking image matching questions directory: {}", str(e))
        
        debug_log("Loaded {} image matching questions", len(self.image_matching_questions))
    
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
            question_id: The ID of the question to retrieve.
            
        Returns:
            Optional[FillInTheBlankQuestion]: The question if found, None otherwise.
        """
        for question in self.fill_in_blank_questions:
            if question.id == question_id:
                return question
        return None
    
    def get_image_matching_question_by_id(self, question_id: int) -> Optional[ImageMatchingQuestion]:
        """
        Get an image matching question by its ID.
        
        Args:
            question_id: The ID of the question to retrieve.
            
        Returns:
            Optional[ImageMatchingQuestion]: The question if found, None otherwise.
        """
        for question in self.image_matching_questions:
            if question.id == question_id:
                return question
        return None 