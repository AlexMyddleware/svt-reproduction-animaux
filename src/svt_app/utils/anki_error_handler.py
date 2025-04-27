"""Error handling utilities for Anki integration."""
from typing import Optional, Dict, Any
import requests
from urllib3.exceptions import NewConnectionError
from ..utils.logging_utils import conditional_log

class AnkiConnectionError(Exception):
    """Custom exception for Anki connection issues."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        """Initialize the error.
        
        Args:
            message: The error message
            details: Additional error details
        """
        super().__init__(message)
        self.details = details or {}

def diagnose_connection_error(error: Exception) -> Dict[str, Any]:
    """Diagnose connection errors and provide detailed information.
    
    Args:
        error: The exception that occurred
        
    Returns:
        Dict containing error diagnosis and suggestions
    """
    diagnosis = {
        'error_type': type(error).__name__,
        'message': str(error),
        'possible_causes': [],
        'suggestions': []
    }
    
    conditional_log("Diagnosing Anki connection error: {}", str(error))
    
    if isinstance(error, requests.exceptions.ConnectionError):
        if isinstance(error.args[0], NewConnectionError):
            diagnosis['possible_causes'].extend([
                "Anki is not running",
                "AnkiConnect add-on is not installed",
                "AnkiConnect is running on a different port",
                "Firewall is blocking the connection"
            ])
            diagnosis['suggestions'].extend([
                "Start Anki application",
                "Install AnkiConnect add-on (code: 2055492159)",
                "Check AnkiConnect port in add-on configuration",
                "Check firewall settings"
            ])
            conditional_log("Connection refused error detected. Possible causes: {}", 
                          diagnosis['possible_causes'])
    
    elif isinstance(error, requests.exceptions.Timeout):
        diagnosis['possible_causes'].append("Connection timeout")
        diagnosis['suggestions'].append("Check if Anki is responding")
        conditional_log("Timeout error detected")
    
    elif isinstance(error, requests.exceptions.RequestException):
        diagnosis['possible_causes'].append("General connection error")
        diagnosis['suggestions'].append("Check network connectivity")
        conditional_log("General request error detected: {}", str(error))
    
    return diagnosis 