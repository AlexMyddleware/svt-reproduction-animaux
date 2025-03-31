"""Test Blueprint creation in game controller."""

from typing import TYPE_CHECKING
import pytest
from flask import Blueprint
from svt_app.controllers.game_controller import game_bp

if TYPE_CHECKING:
    from _pytest.fixtures import FixtureRequest

def test_game_blueprint_creation() -> None:
    """Test that game_bp is correctly created as a Blueprint instance.
    
    Verifies:
    1. game_bp is a Blueprint instance
    2. Blueprint has correct name
    """
    assert isinstance(game_bp, Blueprint)
    assert game_bp.name == "game" 