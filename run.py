"""Entry point script for Révijouer application."""

import os
import sys
import webbrowser
from threading import Timer
import argparse

# Add src directory to Python path
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.insert(0, src_path)

from waitress import serve
from svt_app import create_app
from svt_app.utils.logging_utils import conditional_log, log_if_enabled

@log_if_enabled()
def open_browser() -> None:
    """Open the default web browser to the application URL."""
    conditional_log("Opening browser to http://localhost:8080")
    webbrowser.open('http://localhost:8080')

@log_if_enabled()
def main() -> None:
    """
    Main entry point for the application.
    Sets up the production server and launches the browser.
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Révijouer')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()

    # Set debug mode from command line argument
    debug_mode = args.debug
    if debug_mode:
        os.environ['SVT_DEBUG'] = '1'
        conditional_log("Debug mode enabled via command line")

    # Ensure the data directories exist
    conditional_log("Creating data directories if they don't exist")
    os.makedirs("assets/Data/fill_the_blanks", exist_ok=True)
    os.makedirs("assets/Data/image_matching", exist_ok=True)

    # Create the Flask application
    conditional_log("Creating Flask application")
    app = create_app()
    
    # Open browser after a short delay
    if not debug_mode:  # Don't auto-open browser in debug mode
        Timer(1.5, open_browser).start()
    
    # Run the application with waitress (production server)
    conditional_log("Starting server...")
    print("Starting Révijouer...")
    print("Application running at http://localhost:8080")
    print("Debug mode:", "enabled" if debug_mode else "disabled")
    print("You can close the application by closing this window")
    
    if debug_mode:
        # Use Flask's development server in debug mode
        conditional_log("Starting Flask development server")
        app.run(host='localhost', port=8080, debug=True)
    else:
        # Use waitress in production mode
        conditional_log("Starting Waitress production server")
        serve(app, host='localhost', port=8080)

if __name__ == '__main__':
    main() 