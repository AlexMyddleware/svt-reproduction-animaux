"""Tests for the main menu functionality of the Révijouer application."""

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

def test_main_menu_access(client: "Client") -> None:
    """
    Test access to the main menu of the application.
    
    This test verifies that:
    1. The main menu route ('/') returns a 200 status code
    2. The response contains expected menu elements
    
    Args:
        client: A pytest fixture providing a test client for making requests.
    """
    response = client.get('/')
    assert response.status_code == 200
    
    # Convert response data from bytes to string
    html_content = response.data.decode('utf-8')
    
    # Check for expected menu elements
    assert "Révijouer" in html_content
    assert "Menu Principal" in html_content

def test_main_menu_links(client: "Client") -> None:
    """
    Test that the main menu contains all necessary navigation links.
    
    This test verifies that all expected navigation links are present
    in the main menu HTML.
    
    Args:
        client: A pytest fixture providing a test client for making requests.
    """
    response = client.get('/')
    html_content = response.data.decode('utf-8')
    
    # Check for expected navigation links
    expected_links = [
        "Texte à trous",
        "Relier les images",
        "Créer une question",
        "Gérer les questions",
        "Réinitialiser les scores",
        "Paramètres",
        "Quitter"
    ]
    
    for link in expected_links:
        assert link in html_content, f"Link '{link}' not found in main menu"

def test_score_display(client: "Client") -> None:
    """
    Test that the score section is properly displayed in the main menu.
    
    This test verifies that:
    1. The scores section is present
    2. Both game type scores are displayed
    
    Args:
        client: A pytest fixture providing a test client for making requests.
    """
    response = client.get('/')
    html_content = response.data.decode('utf-8')
    
    # Check for score section
    assert "Scores" in html_content
    assert "Texte à trous: 0" in html_content
    assert "Relier les images: 0" in html_content

def test_score_reset(client: "Client") -> None:
    """
    Test the score reset functionality.
    
    This test verifies that:
    1. The reset scores button works
    2. After reset, 'Texte à trous' score becomes 1
    3. After reset, 'Relier les images' score remains 0
    
    Args:
        client: A pytest fixture providing a test client for making requests.
    """
    # First verify initial scores
    response = client.get('/')
    html_content = response.data.decode('utf-8')
    assert "Texte à trous: 0" in html_content
    assert "Relier les images: 0" in html_content
    
    # Trigger score reset
    response = client.post('/game/reset_scores')
    assert response.status_code == 200
    
    # Verify updated scores
    response = client.get('/')
    html_content = response.data.decode('utf-8')
    assert "Texte à trous: 0" in html_content
    assert "Relier les images: 0" in html_content