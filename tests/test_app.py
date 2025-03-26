"""Basic test module for demonstration."""

from typing import TYPE_CHECKING
import pytest

if TYPE_CHECKING:
    from _pytest.capture import CaptureFixture
    from _pytest.fixtures import FixtureRequest
    from _pytest.logging import LogCaptureFixture
    from _pytest.monkeypatch import MonkeyPatch
    from pytest_mock.plugin import MockerFixture

# Import create_app from your app module
from src.svt_app.app import create_app

@pytest.fixture
def client() -> "pytest.FixtureClient":
    """
    Create a test client for the Flask application.
    
    Returns:
        A test client that can be used to make requests to the application.
    """
    app = create_app()
    return app.test_client()

def test_basic_addition() -> None:
    """
    Test that basic addition works correctly.
    
    This is a simple test to verify that 1 + 1 equals 2.
    """
    result = 1 + 1
    assert result == 2 

def test_app_creation() -> None:
    """
    Test that the app is created correctly.
    """
    app = create_app()
    assert app is not None

def test_hello_route(client: "pytest.FixtureClient") -> None:
    """
    Test the default route of the application.
    
    This test verifies that the application responds correctly to a GET request
    to the root URL ('/') with a 200 status code.
    
    Args:
        client: A pytest fixture that provides a test client for making requests.
    """
    response = client.get('/')
    assert response.status_code == 200

