"""Test module for the scores dictionary in game_controller."""

from typing import Dict
from flask import Flask
from src.svt_app.controllers.game_controller import scores, reset_scores, game_bp


def test_dict_scores_initialization() -> None:
    """
    Test that the scores dictionary is properly initialized.
    
    The scores dictionary should:
    1. Be initialized with two keys: 'texte_a_trous' and 'relier_images'
    2. Both values should be initialized to 0
    """
    expected_scores: Dict[str, int] = {
        "texte_a_trous": 0,
        "relier_images": 0
    }
    assert scores == expected_scores, "Scores dictionary should be initialized with both game types set to 0"


def test_dict_scores_reset() -> None:
    """
    Test that the scores dictionary can be properly reset.
    
    The reset_scores function should:
    1. Reset both scores to 0 regardless of their previous values
    2. Return a success response
    """
    # Create a test Flask app and register the blueprint
    app = Flask(__name__)
    app.register_blueprint(game_bp)

    # Manually modify scores to simulate game progress
    scores["texte_a_trous"] = 5
    scores["relier_images"] = 3
    
    # Use the app context for the test
    with app.test_request_context():
        # Call reset function
        response = reset_scores()
        
        # Verify response
        assert response.json["success"] is True, "Reset scores should return success"
        
        # Verify scores are reset
        assert scores["texte_a_trous"] == 0, "texte_a_trous score should be reset to 0"
        assert scores["relier_images"] == 0, "relier_images score should be reset to 0"


def test_dict_scores_structure() -> None:
    """
    Test the structure and mutability of the scores dictionary.
    
    The scores dictionary should:
    1. Contain exactly two keys
    2. Only accept integer values
    3. Allow score modifications
    """
    # Test dictionary has exactly two keys
    assert len(scores.keys()) == 2, "Scores dictionary should have exactly two keys"
    
    # Test all values are integers
    assert all(isinstance(value, int) for value in scores.values()), "All scores should be integers"
    
    # Test score modification
    original_score = scores["texte_a_trous"]
    scores["texte_a_trous"] += 1
    assert scores["texte_a_trous"] == original_score + 1, "Scores should be modifiable"
