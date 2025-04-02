"""Settings controller module for Révijouer application."""

import json
import os
from typing import Dict, Any
from flask import Blueprint, render_template, request, jsonify, session

from svt_app.utils.debug import debug_log

# Create a Blueprint for the settings routes
settings_bp = Blueprint("settings", __name__)

# Settings file path
SETTINGS_FILE = "assets/settings.json"

def load_settings() -> Dict[str, Any]:
    """
    Load settings from the settings file.
    
    Returns:
        Dict[str, Any]: Dictionary containing the settings.
    """
    default_settings = {
        "auto_validate": True
    }
    
    if not os.path.exists(SETTINGS_FILE):
        # Create settings file with default values
        os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_settings, f, indent=4)
        debug_log("Created new settings file with default values")
        return default_settings
    
    try:
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            settings = json.load(f)
            # Ensure all default settings exist
            for key, value in default_settings.items():
                if key not in settings:
                    settings[key] = value
            debug_log("Loaded settings: {}", settings)
            return settings
    except Exception as e:
        debug_log("Error loading settings: {}", str(e))
        return default_settings

def save_settings(settings: Dict[str, Any]) -> bool:
    """
    Save settings to the settings file.
    
    Args:
        settings: Dictionary containing the settings to save.
        
    Returns:
        bool: True if settings were saved successfully, False otherwise.
    """
    try:
        os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=4)
        debug_log("Saved settings: {}", settings)
        return True
    except Exception as e:
        debug_log("Error saving settings: {}", str(e))
        return False

@settings_bp.route("/")
def settings() -> str:
    """
    Render the settings page.
    
    Returns:
        str: Rendered HTML template for the settings page.
    """
    settings_data = load_settings()
    debug_log("Rendering settings page with data: {}", settings_data)
    return render_template("settings.html", auto_validate=settings_data.get("auto_validate", True))

@settings_bp.route("/save", methods=["POST"])
def save() -> Dict[str, Any]:
    """
    Save settings.
    
    Returns:
        Dict[str, Any]: JSON response indicating success or failure.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "No data provided"})
        
        current_settings = load_settings()
        current_settings["auto_validate"] = bool(data.get("auto_validate", True))
        debug_log("Saving new settings: {}", current_settings)
        
        if save_settings(current_settings):
            return jsonify({"success": True, "message": "Paramètres enregistrés avec succès"})
        else:
            return jsonify({"success": False, "message": "Une erreur est survenue lors de l'enregistrement des paramètres"})
    
    except Exception as e:
        debug_log("Error saving settings: {}", str(e))
        return jsonify({"success": False, "message": "Une erreur est survenue lors de l'enregistrement des paramètres"}) 