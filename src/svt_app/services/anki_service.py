"""Service for interacting with Anki through AnkiConnect."""
from typing import Any, Dict, Optional, Tuple
import json
import requests
from typing import TypedDict

from ..config.anki_config import AnkiConfig
from ..utils.logging_utils import conditional_log
from ..utils.anki_error_handler import diagnose_connection_error

class AnkiResponse(TypedDict):
    """Type definition for Anki API response."""
    result: Optional[Any]
    error: Optional[str]

class AnkiService:
    """Service class for interacting with Anki through AnkiConnect."""

    def __init__(self) -> None:
        """Initialize the AnkiService using configuration."""
        self.endpoint = AnkiConfig.get_api_endpoint()
        self.email, self.password = AnkiConfig.get_credentials()
        conditional_log("AnkiService initialized with endpoint: {}", self.endpoint)
        conditional_log("Using email: {}", self.email if self.email else "Not set")

    def _make_request(self, action: str, params: Dict[str, Any] = {}) -> Tuple[Optional[AnkiResponse], Optional[Dict[str, Any]]]:
        """Make a request to the Anki API.
        
        Args:
            action: The AnkiConnect action to perform
            params: Parameters for the action
            
        Returns:
            Tuple of (response data, error diagnosis) if error occurs
            
        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        payload = {
            "action": action,
            "version": 6,
            "params": params
        }
        
        conditional_log("Making Anki API request: action={}, params={}", action, params)
        
        try:
            response = requests.post(self.endpoint, json=payload, timeout=5)
            response_data = response.json()
            conditional_log("Anki API response: {}", response_data)
            return response_data, None
        except requests.exceptions.RequestException as e:
            error_diagnosis = diagnose_connection_error(e)
            conditional_log("Anki API request failed: {}", error_diagnosis)
            return None, error_diagnosis

    def authenticate(self) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """Authenticate with Anki using credentials.
        
        Returns:
            Tuple of (success status, error diagnosis if any)
        """
        if not self.email or not self.password:
            conditional_log("Missing Anki credentials")
            return False, {
                'error_type': 'ConfigError',
                'message': 'Missing credentials',
                'possible_causes': ['Credentials not set in .env.local'],
                'suggestions': ['Add ANKI_EMAIL and ANKI_PASSWORD to .env.local']
            }

        try:
            conditional_log("Attempting Anki authentication with email: {}", self.email)
            is_connected, error_diagnosis = self.test_connection()
            if is_connected:
                conditional_log("Anki authentication successful")
                return True, None
            else:
                conditional_log("Anki authentication failed")
                return False, error_diagnosis
        except Exception as e:
            error_diagnosis = {
                'error_type': type(e).__name__,
                'message': str(e),
                'possible_causes': ['Unexpected error during authentication'],
                'suggestions': ['Check application logs for details']
            }
            conditional_log("Anki authentication error: {}", str(e), level='ERROR')
            return False, error_diagnosis

    def test_connection(self) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """Test the connection to Anki.
        
        Returns:
            Tuple of (success status, error diagnosis if any)
        """
        try:
            conditional_log("Testing Anki connection")
            response, error_diagnosis = self._make_request("version")
            
            if response and "result" in response and response.get("error") is None:
                conditional_log("Anki connection test successful")
                return True, None
            else:
                conditional_log("Anki connection test failed: invalid response")
                return False, error_diagnosis
        except Exception as e:
            error_diagnosis = diagnose_connection_error(e)
            conditional_log("Anki connection test failed: {}", str(e), level='ERROR')
            return False, error_diagnosis

    def get_deck_names(self) -> list[str]:
        """Get all available deck names.
        
        Returns:
            List of deck names
            
        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        conditional_log("Fetching Anki deck names")
        response = self._make_request("deckNames")
        decks = response.get("result", [])
        conditional_log("Retrieved {} Anki decks", len(decks))
        return decks 