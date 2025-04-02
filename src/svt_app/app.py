"""Main application module for Révijouer."""

from typing import Dict, Any, Optional
from flask import Flask, render_template, request, redirect, url_for, session
import secrets

from svt_app.controllers.game_controller import game_bp
from svt_app.controllers.settings_controller import settings_bp
from svt_app.controllers.image_matching_controller import image_matching_bp
from svt_app.utils.debug import debug_log, DEBUG_MODE
from svt_app.state import GameScores

def create_app() -> Flask:
    """
    Create and configure the Flask application.
    
    Returns:
        Flask: The configured Flask application instance.
    """
    debug_log("Creating Flask application")
    app = Flask(__name__)
    
    # Generate a secure random secret key
    app.secret_key = secrets.token_hex(32)
    app.config['SESSION_TYPE'] = 'filesystem'
    
    debug_log("Debug mode is {}", "enabled" if DEBUG_MODE else "disabled")

    @app.before_request
    def before_request() -> None:
        """Log session data before each request."""
        debug_log("Session before request: {}", dict(session))

    @app.after_request
    def after_request(response: Any) -> Any:
        """Log session data after each request."""
        debug_log("Session after request: {}", dict(session))
        return response

    # Register blueprints
    debug_log("Registering blueprints")
    app.register_blueprint(game_bp, url_prefix="/game")
    app.register_blueprint(settings_bp, url_prefix="/settings")
    app.register_blueprint(image_matching_bp, url_prefix="/game")

    @app.route("/")
    def index() -> str:
        """
        Render the main menu page.
        
        Returns:
            str: Rendered HTML template for the main menu.
        """
        debug_log("Rendering index page")
        scores = GameScores.get_scores()
        debug_log("Current scores for index page: {}", scores)
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