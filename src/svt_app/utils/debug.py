"""Debug utility module for SVT Reproduction Animaux application."""

from typing import Any
import os
from functools import wraps
import logging

# Initialize debug mode from environment variable
DEBUG_MODE = os.environ.get('SVT_DEBUG', '0').lower() in ('1', 'true', 'yes')

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if DEBUG_MODE else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('svt_app')

def debug_log(message: str, *args: Any, **kwargs: Any) -> None:
    """
    Log a debug message if debug mode is enabled.
    
    Args:
        message: The message to log
        *args: Additional positional arguments for string formatting
        **kwargs: Additional keyword arguments for string formatting
    """
    if DEBUG_MODE:
        formatted_message = message.format(*args, **kwargs) if args or kwargs else message
        logger.debug(formatted_message)

def debug_only(func: Any) -> Any:
    """
    Decorator to run a function only in debug mode.
    
    Args:
        func: The function to decorate
        
    Returns:
        The decorated function that only runs in debug mode
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if DEBUG_MODE:
            return func(*args, **kwargs)
        return None
    return wrapper 