"""Configuration for Anki integration."""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env.local
load_dotenv('.env.local')

class AnkiConfig:
    """Configuration class for Anki settings."""
    
    @staticmethod
    def get_credentials() -> tuple[Optional[str], Optional[str]]:
        """Get Anki credentials from environment variables.
        
        Returns:
            tuple: (email, password) from environment variables
        """
        return (
            os.getenv('ANKI_EMAIL'),
            os.getenv('ANKI_PASSWORD')
        )
    
    @staticmethod
    def get_api_endpoint() -> str:
        """Get AnkiConnect API endpoint.
        
        Returns:
            str: The API endpoint URL
        """
        host = os.getenv('ANKI_HOST', 'localhost')
        port = os.getenv('ANKI_PORT', '8765')
        return f"http://{host}:{port}" 