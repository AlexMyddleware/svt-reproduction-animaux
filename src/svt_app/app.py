"""Main application module for SVT Reproduction Animaux."""

from typing import Dict, Any, Optional
from flask import Flask, render_template, request, redirect, url_for, session

from svt_app.controllers.game_controller import game_bp
from svt_app.controllers.settings_controller import settings_bp
from svt_app.utils.debug import debug_log, DEBUG_MODE

def create_app() -> Flask:
    """
    Create and configure the Flask application.
    
    Returns:
        Flask: The configured Flask application instance.
    """
    debug_log("Creating Flask application")
    app = Flask(__name__)
    app.secret_key = "svt_reproduction_animaux_secret_key"  # For session management
    
    debug_log("Debug mode is {}", "enabled" if DEBUG_MODE else "disabled")

    # Register blueprints
    debug_log("Registering blueprints")
    app.register_blueprint(game_bp, url_prefix="/game")
    app.register_blueprint(settings_bp, url_prefix="/settings")

    @app.route("/")
    def index() -> str:
        """
        Render the main menu page.
        
        Returns:
            str: Rendered HTML template for the main menu.
        """
        debug_log("Rendering index page")
        from svt_app.controllers.game_controller import scores
        return render_template("index.html", scores=scores)

    @app.route("/settings")
    def settings() -> str:
        """
        Render the settings page.
        
        Returns:
            str: Rendered HTML template for the settings page.
        """
        debug_log("Rendering settings page")
        return render_template("settings.html")

    @app.route("/quit")
    def quit_app() -> str:
        """
        Handle the quit action.
        
        In a web application, this typically redirects to a goodbye page
        or back to the main menu.
        
        Returns:
            str: Redirect to the main menu.
        """
        debug_log("Handling quit action")
        return redirect(url_for("index"))

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=DEBUG_MODE) 