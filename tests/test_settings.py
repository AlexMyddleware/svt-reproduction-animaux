"""Tests for the settings page functionality."""

from typing import TYPE_CHECKING
import pytest
import json

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
    
    assert "Révijouer" in html_content
    assert "Paramètres" in html_content

def test_settings_page_elements(client: "Client") -> None:
    """
    Test that all required elements are present on the settings page.
    
    This test verifies that all sections and their content are properly displayed:
    - Font family section
    - Language section
    - Question validation section
    - About section
    - Return to menu button
    
    Args:
        client: A pytest fixture providing a test client for making requests.
    """
    response = client.get('/settings')
    html_content = response.data.decode('utf-8')
    
    # Font family section
    assert "Police de caractères" in html_content
    assert "Choisissez la police de caractères utilisée dans toute l'application." in html_content
    assert "Atkinson Hyperlegible" in html_content
    assert "Orbitron" in html_content
    
    # Language section
    assert "Langue" in html_content
    assert "Toutes les questions sont en français." in html_content
    
    # Question validation section
    assert "Validation des questions" in html_content
    assert "Marquer automatiquement une question comme validée lorsqu'elle est correctement répondue" in html_content
    
    # About section
    assert "À propos" in html_content
    assert "Révijouer - Version 1.0" in html_content
    assert "Une application éducative pour apprendre sur la reproduction des animaux." in html_content
    
    # Navigation
    assert "Retour au menu" in html_content

def test_font_family_dropdown_options(client: "Client") -> None:
    """
    Test that the font family dropdown contains all expected options.
    
    Args:
        client: A pytest fixture providing a test client for making requests.
    """
    response = client.get('/settings')
    html_content = response.data.decode('utf-8')
    
    # Check that all font options are present
    expected_fonts = [
        "Atkinson Hyperlegible",
        "Orbitron", 
        "serif",
        "sans-serif",
        "monospace",
        "cursive",
        "fantasy"
    ]
    
    for font in expected_fonts:
        assert f'value="{font}"' in html_content

def test_get_font_endpoint(client: "Client") -> None:
    """
    Test the /settings/get-font endpoint returns the current font setting.
    
    Args:
        client: A pytest fixture providing a test client for making requests.
    """
    response = client.get('/settings/get-font')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'font_family' in data
    assert isinstance(data['font_family'], str)

def test_save_font_setting(client: "Client") -> None:
    """
    Test saving font family setting through the API.
    
    Args:
        client: A pytest fixture providing a test client for making requests.
    """
    # Test saving Orbitron font
    response = client.post('/settings/save', 
                          json={'auto_validate': True, 'font_family': 'Orbitron'},
                          content_type='application/json')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['success'] is True
    
    # Verify the setting was saved by checking the get-font endpoint
    response = client.get('/settings/get-font')
    data = json.loads(response.data)
    assert data['font_family'] == 'Orbitron'

def test_save_all_font_families(client: "Client") -> None:
    """
    Test saving each available font family option.
    
    Args:
        client: A pytest fixture providing a test client for making requests.
    """
    font_families = [
        "Atkinson Hyperlegible",
        "Orbitron",
        "serif",
        "sans-serif", 
        "monospace",
        "cursive",
        "fantasy"
    ]
    
    for font_family in font_families:
        # Save the font family
        response = client.post('/settings/save',
                              json={'auto_validate': True, 'font_family': font_family},
                              content_type='application/json')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        
        # Verify it was saved correctly
        response = client.get('/settings/get-font')
        data = json.loads(response.data)
        assert data['font_family'] == font_family

def test_invalid_font_family_handling(client: "Client") -> None:
    """
    Test that invalid font family values are handled gracefully.
    
    Args:
        client: A pytest fixture providing a test client for making requests.
    """
    # Test with an invalid font family
    response = client.post('/settings/save',
                          json={'auto_validate': True, 'font_family': 'InvalidFont'},
                          content_type='application/json')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['success'] is True  # Should still save, validation is client-side

def test_font_manager_css_inclusion(client: "Client") -> None:
    """
    Test that the font manager CSS is included in the settings page.
    
    Args:
        client: A pytest fixture providing a test client for making requests.
    """
    response = client.get('/settings')
    html_content = response.data.decode('utf-8')
    
    assert 'css/font_manager.css' in html_content

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