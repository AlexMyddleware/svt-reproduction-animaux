"""Tests for the question service module."""

import os
import json
import tempfile
from typing import Dict, Any, List, Optional
from pathlib import Path
import pytest
from _pytest.capture import CaptureFixture
from _pytest.fixtures import FixtureRequest
from _pytest.logging import LogCaptureFixture
from _pytest.monkeypatch import MonkeyPatch
from pytest_mock.plugin import MockerFixture

from src.svt_app.services.question_service import QuestionService
from src.svt_app.models.question import FillInTheBlankQuestion, ImageMatchingQuestion


@pytest.fixture
def temp_fill_blanks_dir() -> str:
    """
    Create a temporary directory for fill-in-the-blank questions.
    
    Returns:
        str: Path to the temporary directory.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        fill_blanks_dir = os.path.join(temp_dir, "fill_the_blanks")
        os.makedirs(fill_blanks_dir, exist_ok=True)
        
        # Create a sample question
        question_data = {
            "text": "La reproduction sexuée chez les grenouilles implique ________ qui se rencontrent dans l'eau.",
            "options": [
                "des gamètes",
                "des cellules",
                "des œufs",
                "des embryons"
            ],
            "correct_answer": "des gamètes"
        }
        
        with open(os.path.join(fill_blanks_dir, "question1.json"), "w", encoding="utf-8") as f:
            json.dump(question_data, f, ensure_ascii=False)
        
        yield temp_dir


@pytest.fixture
def temp_image_matching_dir() -> str:
    """
    Create a temporary directory for image matching questions.
    
    Returns:
        str: Path to the temporary directory.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        image_matching_dir = os.path.join(temp_dir, "image_interaction")
        os.makedirs(image_matching_dir, exist_ok=True)
        
        # Create a sample question
        question_data = {
            "image": "assets/images/image_interaction/question1.png",
            "words": {
                "correct": "deux espèces différentes de grenouille",
                "incorrect": [
                    "Un mâle et une femelle grenouille",
                    "Une grenouille et un crapaud",
                    "Une salamandre et une grenouille",
                    "Un triton et un tétard"
                ]
            }
        }
        
        with open(os.path.join(image_matching_dir, "question1.json"), "w", encoding="utf-8") as f:
            json.dump(question_data, f, ensure_ascii=False)
        
        yield temp_dir


def test_load_fill_in_blank_questions(temp_fill_blanks_dir: str, monkeypatch: MonkeyPatch) -> None:
    """
    Test loading fill-in-the-blank questions.
    
    Args:
        temp_fill_blanks_dir: Temporary directory with fill-in-the-blank questions.
        monkeypatch: Pytest monkeypatch fixture.
    """
    # Patch the Path to use our temporary directory
    def mock_path_init(self, *args, **kwargs):
        if args and args[0] == "assets/Data/fill_the_blanks":
            self.path = Path(os.path.join(temp_fill_blanks_dir, "fill_the_blanks"))
        else:
            self.path = Path(*args, **kwargs)
        
        self.exists = lambda: self.path.exists()
        self.glob = lambda pattern: self.path.glob(pattern)
        self.stem = self.path.stem
    
    monkeypatch.setattr(Path, "__init__", mock_path_init)
    monkeypatch.setattr(Path, "__new__", lambda cls, *args, **kwargs: object.__new__(cls))
    
    # Create the service and test loading questions
    service = QuestionService()
    
    # Check that the question was loaded
    assert len(service.fill_in_blank_questions) == 1
    
    question = service.fill_in_blank_questions[0]
    assert question.id == 1
    assert "grenouilles" in question.text
    assert "des gamètes" in question.options
    assert question.correct_answer == "des gamètes"


def test_load_image_matching_questions(temp_image_matching_dir: str, monkeypatch: MonkeyPatch) -> None:
    """
    Test loading image matching questions.
    
    Args:
        temp_image_matching_dir: Temporary directory with image matching questions.
        monkeypatch: Pytest monkeypatch fixture.
    """
    # Patch the Path to use our temporary directory
    def mock_path_init(self, *args, **kwargs):
        if args and args[0] == "assets/Data/image_interaction":
            self.path = Path(os.path.join(temp_image_matching_dir, "image_interaction"))
        else:
            self.path = Path(*args, **kwargs)
        
        self.exists = lambda: self.path.exists()
        self.glob = lambda pattern: self.path.glob(pattern)
        self.stem = self.path.stem
    
    monkeypatch.setattr(Path, "__init__", mock_path_init)
    monkeypatch.setattr(Path, "__new__", lambda cls, *args, **kwargs: object.__new__(cls))
    
    # Create the service and test loading questions
    service = QuestionService()
    
    # Check that the question was loaded
    assert len(service.image_matching_questions) == 1
    
    question = service.image_matching_questions[0]
    assert question.id == 1
    assert question.image_path == "assets/images/image_interaction/question1.png"
    assert question.correct_word == "deux espèces différentes de grenouille"
    assert len(question.incorrect_words) == 4
    assert "Un mâle et une femelle grenouille" in question.incorrect_words


def test_get_question_by_id() -> None:
    """Test getting questions by ID."""
    service = QuestionService()
    
    # Add mock questions
    service.fill_in_blank_questions = [
        FillInTheBlankQuestion(id=1, text="Question 1", options=["A", "B"], correct_answer="A"),
        FillInTheBlankQuestion(id=2, text="Question 2", options=["C", "D"], correct_answer="D")
    ]
    
    service.image_matching_questions = [
        ImageMatchingQuestion(id=1, image_path="path1.png", correct_word="Word1", incorrect_words=["Word2"]),
        ImageMatchingQuestion(id=2, image_path="path2.png", correct_word="Word3", incorrect_words=["Word4"])
    ]
    
    # Test getting fill-in-the-blank questions by ID
    question = service.get_fill_in_blank_question_by_id(1)
    assert question is not None
    assert question.id == 1
    assert question.text == "Question 1"
    
    question = service.get_fill_in_blank_question_by_id(3)  # Non-existent ID
    assert question is None
    
    # Test getting image matching questions by ID
    question = service.get_image_matching_question_by_id(2)
    assert question is not None
    assert question.id == 2
    assert question.image_path == "path2.png"
    
    question = service.get_image_matching_question_by_id(3)  # Non-existent ID
    assert question is None 