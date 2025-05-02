"""Main application module for Révijouer."""

from typing import Dict, Any, Optional
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import secrets
import os
import threading

from svt_app.controllers.game_controller import game_bp
from svt_app.controllers.settings_controller import settings_bp
from svt_app.controllers.image_matching_controller import image_matching_bp
from svt_app.routes.anki_routes import anki_bp
from svt_app.routes.anki_training_routes import training_bp
from svt_app.utils.logging_utils import conditional_log, log_if_enabled
from svt_app.state import GameScores

@log_if_enabled()
def create_app() -> Flask:
    """
    Create and configure the Flask application.
    
    Returns:
        Flask: The configured Flask application instance.
    """
    conditional_log("Creating Flask application")
    app = Flask(__name__)
    
    # Generate a secure random secret key
    app.secret_key = secrets.token_hex(32)
    app.config['SESSION_TYPE'] = 'filesystem'
    
    conditional_log("Debug mode is {}", app.debug)

    @app.before_request
    def before_request() -> None:
        """Log session data before each request."""
        conditional_log("Session before request: {}", dict(session))

    @app.after_request
    def after_request(response: Any) -> Any:
        """Log session data after each request."""
        conditional_log("Session after request: {}", dict(session))
        return response

    # Register blueprints
    conditional_log("Registering blueprints")
    app.register_blueprint(game_bp, url_prefix="/game")
    app.register_blueprint(settings_bp, url_prefix="/settings")
    app.register_blueprint(image_matching_bp, url_prefix="/game")
    app.register_blueprint(anki_bp, url_prefix="/")
    app.register_blueprint(training_bp, url_prefix="/")

    @app.route("/")
    @log_if_enabled()
    def index() -> str:
        """
        Render the main menu page.
        
        Returns:
            str: Rendered HTML template for the main menu.
        """
        conditional_log("Rendering index page")
        scores = GameScores.get_scores()
        conditional_log("Current scores for index page: {}", scores)
        return render_template("index.html", scores=scores)

    @app.route("/quit")
    @log_if_enabled()
    def quit_app() -> str:
        """
        Handle the quit action.
        
        Shuts down the application by terminating the Python process
        after a short delay to allow the response to be sent.
        
        Returns:
            str: JSON response indicating success.
        """
        conditional_log("Handling quit action")
        
        def delayed_shutdown():
            # Wait a short moment to allow the response to be sent
            threading.Timer(0.5, lambda: os._exit(0)).start()
        
        try:
            # Start the delayed shutdown
            delayed_shutdown()
            return jsonify({"success": True})
        except Exception as e:
            conditional_log("Error during shutdown: {}", str(e))
            return jsonify({"success": False, "error": str(e)})

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True) 