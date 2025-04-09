"""Logging utilities for the SVT application."""

import os
import json
import logging
from functools import wraps
from typing import Any, Callable, Dict, Optional, Union

# Load logging configuration
def load_logging_config() -> Dict[str, Any]:
    """
    Load logging configuration from JSON file.
    
    Returns:
        Dict[str, Any]: The logging configuration dictionary.
    """
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'logging_config.json')
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading logging config: {e}")
        return {
            "version": 1,
            "enabled_loggers": {},
            "log_level": "INFO",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "date_format": "%Y-%m-%d %H:%M:%S"
        }

# Global configuration
_CONFIG = load_logging_config()

def get_logger(module_name: str) -> logging.Logger:
    """
    Get a logger instance for the specified module.
    
    Args:
        module_name: The name of the module requesting the logger.
        
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(module_name)
    
    # Only configure if not already configured
    if not logger.handlers:
        logger.setLevel(getattr(logging, _CONFIG.get('log_level', 'INFO')))
        
        # Create console handler
        handler = logging.StreamHandler()
        handler.setLevel(getattr(logging, _CONFIG.get('log_level', 'INFO')))
        
        # Create formatter
        formatter = logging.Formatter(
            fmt=_CONFIG.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
            datefmt=_CONFIG.get('date_format', '%Y-%m-%d %H:%M:%S')
        )
        
        # Add formatter to handler
        handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(handler)
        
        # Set propagate to False to avoid duplicate logs
        logger.propagate = False
    
    return logger

def is_logging_enabled(module_name: str) -> bool:
    """
    Check if logging is enabled for the specified module.
    
    Args:
        module_name: The name of the module to check.
        
    Returns:
        bool: True if logging is enabled, False otherwise.
    """
    enabled_loggers = _CONFIG.get('enabled_loggers', {})
    return enabled_loggers.get(module_name, False)

def log_if_enabled(level: str = 'DEBUG') -> Callable:
    """
    Decorator that logs function calls if logging is enabled for the module.
    
    Args:
        level: The logging level to use. Defaults to 'DEBUG'.
        
    Returns:
        Callable: The decorator function.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            module_name = func.__module__
            if is_logging_enabled(module_name):
                logger = get_logger(module_name)
                log_method = getattr(logger, level.lower())
                log_method(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
                try:
                    result = func(*args, **kwargs)
                    log_method(f"{func.__name__} returned: {result}")
                    return result
                except Exception as e:
                    logger.error(f"Error in {func.__name__}: {e}")
                    raise
            return func(*args, **kwargs)
        return wrapper
    return decorator

def conditional_log(message: str, *args: Any, level: str = 'DEBUG', module_name: Optional[str] = None) -> None:
    """
    Log a message if logging is enabled for the module.
    
    Args:
        message: The message to log.
        *args: Arguments to format the message with.
        level: The logging level to use. Defaults to 'DEBUG'.
        module_name: Optional module name. If not provided, will try to determine from caller.
    """
    if module_name is None:
        import inspect
        frame = inspect.currentframe()
        if frame is not None:
            frame = frame.f_back
            if frame is not None:
                module_name = frame.f_globals['__name__']
    
    if module_name and is_logging_enabled(module_name):
        logger = get_logger(module_name)
        log_method = getattr(logger, level.lower())
        if args:
            try:
                formatted_message = message.format(*args)
            except Exception:
                formatted_message = f"{message} (args={args})"
            log_method(formatted_message)
        else:
            log_method(message) 