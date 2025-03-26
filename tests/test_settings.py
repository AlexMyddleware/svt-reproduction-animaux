"""Tests for the settings page functionality."""

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

def test_settings_page_access(client: "Client") -> None:
    """
    Test that the settings page is accessible and returns 200 status code.
    
    Args:
        client: A pytest fixture providing a test client for making requests.
    """
    response = client.get('/settings')
    assert response.status_code == 200

def test_settings_page_title(client: "Client") -> None:
    """
    Test that the settings page contains the correct title and header.
    
    Args:
        client: A pytest fixture providing a test client for making requests.
    """
    response = client.get('/settings')
    html_content = response.data.decode('utf-8')
    
    assert "SVT Reproduction Animaux" in html_content
    assert "Paramètres" in html_content

def test_settings_page_elements(client: "Client") -> None:
    """
    Test that all required elements are present on the settings page.
    
    This test verifies that all sections and their content are properly displayed:
    - Language section
    - Question validation section
    - About section
    - Return to menu button
    
    Args:
        client: A pytest fixture providing a test client for making requests.
    """
    response = client.get('/settings')
    html_content = response.data.decode('utf-8')
    
    # Language section
    assert "Langue" in html_content
    assert "Toutes les questions sont en français." in html_content
    
    # Question validation section
    assert "Validation des questions" in html_content
    assert "Marquer automatiquement une question comme validée lorsqu'elle est correctement répondue" in html_content
    
    # About section
    assert "À propos" in html_content
    assert "SVT Reproduction Animaux - Version 1.0" in html_content
    assert "Une application éducative pour apprendre sur la reproduction des animaux." in html_content
    
    # Navigation
    assert "Retour au menu" in html_content

def test_settings_return_to_menu(client: "Client") -> None:
    """
    Test that the 'Return to menu' button leads back to the main menu.
    
    Args:
        client: A pytest fixture providing a test client for making requests.
    """
    # First, verify the link exists
    response = client.get('/settings')
    html_content = response.data.decode('utf-8')
    assert 'href="/"' in html_content or 'href="/menu"' in html_content
    
    # Then follow the link
    response = client.get('/')
    assert response.status_code == 200
    menu_content = response.data.decode('utf-8')
    assert "Menu Principal" in menu_content 