"""Tests for question creation functionality."""

import json
import os
from typing import TYPE_CHECKING
import pytest

if TYPE_CHECKING:
    from _pytest.capture import CaptureFixture
    from _pytest.fixtures import FixtureRequest
    from _pytest.logging import LogCaptureFixture
    from _pytest.monkeypatch import MonkeyPatch
    from pytest_mock.plugin import MockerFixture
    from pytest.FixtureClient import Client

from src.svt_app.app import create_app

@pytest.fixture
def client() -> "Client":
    """
    Create a test client for the Flask application.
    
    Returns:
        Client: A test client that can be used to make requests to the application.
    """
    app = create_app()
    return app.test_client()

def test_create_fill_in_blank_question(client: "Client") -> None:
    """
    Test creating a new fill-in-the-blank question.
    
    This test verifies that:
    1. The question can be created via POST request
    2. The question is properly saved to JSON
    3. The question data matches what was sent
    
    Args:
        client: A pytest fixture providing a test client for making requests.
    """
    # Test data
    question_data = {
        "game_type": "texte_a_trous",
        "text": "Les grenouilles sont des ________ qui vivent dans l'eau.",
        "options": ["amphibiens", "reptiles", "poissons", "mammifères"],
        "correct_answer": "amphibiens"
    }
    
    # Send request to create question
    response = client.post('/game/save_question', 
                         json=question_data,
                         content_type='application/json')
    
    # Check response
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data["success"] is True
    
    # Verify the question was saved
    base_dir = "assets/Data/fill_the_blanks"
    files = [f for f in os.listdir(base_dir) if f.startswith("question") and f.endswith(".json")]
    assert len(files) > 0
    
    # Get the latest question file
    latest_file = max(files, key=lambda x: int(x[8:11]))
    file_path = os.path.join(base_dir, latest_file)
    
    # Read and verify the saved question
    with open(file_path, 'r', encoding='utf-8') as f:
        saved_question = json.load(f)
        assert saved_question["text"] == question_data["text"]
        assert saved_question["options"] == question_data["options"]
        assert saved_question["correct_answer"] == question_data["correct_answer"]
    
    # Clean up - remove the test question file
    os.remove(file_path)

def test_create_image_matching_question(client: "Client") -> None:
    """
    Test creating a new image matching question.
    
    This test verifies that:
    1. The question can be created via POST request
    2. The question is properly saved to JSON
    3. The question data matches what was sent
    
    Args:
        client: A pytest fixture providing a test client for making requests.
    """
    # Test data with a simple base64 image
    question_data = {
        "game_type": "relier_images",
        "text": "Identifiez l'animal dans l'image",
        "correct_word": "grenouille",
        "incorrect_words": ["crapaud", "salamandre", "triton"],
        "image_path": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
    }
    
    # Send request to create question
    response = client.post('/game/save_question', 
                         json=question_data,
                         content_type='application/json')
    
    # Check response
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data["success"] is True
    
    # Verify the question was saved
    base_dir = "assets/Data/image_matching"
    files = [f for f in os.listdir(base_dir) if f.startswith("question") and f.endswith(".json")]
    assert len(files) > 0
    
    # Get the latest question file
    latest_file = max(files, key=lambda x: int(x[8:11]))
    file_path = os.path.join(base_dir, latest_file)
    
    # Read and verify the saved question
    with open(file_path, 'r', encoding='utf-8') as f:
        saved_question = json.load(f)
        assert saved_question["text"] == question_data["text"]
        assert saved_question["correct_word"] == question_data["correct_word"]
        assert saved_question["incorrect_words"] == question_data["incorrect_words"]
        assert "image_path" in saved_question
    
    # Clean up - remove the test question file
    os.remove(file_path) 