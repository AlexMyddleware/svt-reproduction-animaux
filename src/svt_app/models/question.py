"""Question model module for Révijouer application."""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class FillInTheBlankQuestion:
    """
    Represents a fill-in-the-blank question.
    
    Attributes:
        id (int): Unique identifier for the question.
        text (str): The question text with blanks represented as underscores.
        options (List[str]): List of possible answers to choose from.
        correct_answer (str): The correct answer for the blank.
    """
    id: int
    text: str
    options: List[str]
    correct_answer: str


@dataclass
class ImageMatchingQuestion:
    """
    Represents an image matching question.
    
    Attributes:
        id (int): Unique identifier for the question.
        image_path (str): Path to the central image.
        correct_word (str): The correct word to match with the image.
        incorrect_words (List[str]): List of incorrect words.
    """
    id: int
    image_path: str
    correct_word: str
    incorrect_words: List[str] 