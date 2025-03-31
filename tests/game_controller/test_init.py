"""Test initialization of game controller components."""

from typing import TYPE_CHECKING
import pytest
from flask import Blueprint
from svt_app.services.question_service import QuestionService

if TYPE_CHECKING:
    from pytest_mock.plugin import MockerFixture

def test_blueprint_creation() -> None:
    """Test that game blueprint can be created correctly."""
    bp = Blueprint("game", __name__)
    assert isinstance(bp, Blueprint)
    assert bp.name == "game"

def test_question_service_creation() -> None:
    """Test that question service can be created correctly."""
    service = QuestionService()
    assert isinstance(service, QuestionService) 