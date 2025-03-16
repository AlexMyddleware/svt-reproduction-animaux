"""Tests for the SVT Reproduction Animaux application."""

from typing import Dict, Any, Optional
import pytest
from _pytest.capture import CaptureFixture
from _pytest.fixtures import FixtureRequest
from _pytest.logging import LogCaptureFixture
from _pytest.monkeypatch import MonkeyPatch
from pytest_mock.plugin import MockerFixture

from src.svt_app.app import app


@pytest.fixture
def client():
    """
    Create a test client for the Flask application.
    
    Returns:
        FlaskClient: A test client for the Flask application.
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index_route(client) -> None:
    """
    Test that the index route returns a 200 status code and contains the expected content.
    
    Args:
        client: The Flask test client.
    """
    response = client.get('/')
    assert response.status_code == 200
    assert b'Menu Principal' in response.data
    assert b'Texte' in response.data
    assert b'Relier les images' in response.data


def test_settings_route(client) -> None:
    """
    Test that the settings route returns a 200 status code and contains the expected content.
    
    Args:
        client: The Flask test client.
    """
    response = client.get('/settings')
    assert response.status_code == 200
    assert b'Param' in response.data  # 'Paramètres' with UTF-8 encoding might be tricky in tests


def test_quit_route(client) -> None:
    """
    Test that the quit route redirects to the index page.
    
    Args:
        client: The Flask test client.
    """
    response = client.get('/quit')
    assert response.status_code == 302  # Redirect status code
    assert response.headers['Location'] == '/'


def test_reset_scores(client) -> None:
    """
    Test that the reset_scores route resets the scores and redirects to the index page.
    
    Args:
        client: The Flask test client.
    """
    # First, access the game routes to potentially increase scores
    client.get('/game/texte_a_trous')
    client.get('/game/relier_images')
    
    # Then reset scores
    response = client.get('/game/reset_scores')
    assert response.status_code == 302  # Redirect status code
    assert response.headers['Location'] == '/'
    
    # Check that scores are reset by accessing the index page
    response = client.get('/')
    assert b'Texte' in response.data
    assert b'Relier les images' in response.data
    assert b'0' in response.data  # Check for score value 