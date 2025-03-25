"""Entry point script for SVT Reproduction Animaux application."""

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
from svt_app.utils.debug import debug_log, DEBUG_MODE

def open_browser() -> None:
    """Open the default web browser to the application URL."""
    webbrowser.open('http://localhost:8080')

def main() -> None:
    """
    Main entry point for the application.
    Sets up the production server and launches the browser.
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='SVT Reproduction Animaux')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()

    # Set debug mode from command line argument
    if args.debug:
        os.environ['SVT_DEBUG'] = '1'
        debug_log("Debug mode enabled via command line")

    # Ensure the data directories exist
    debug_log("Creating data directories if they don't exist")
    os.makedirs("assets/Data/fill_the_blanks", exist_ok=True)
    os.makedirs("assets/Data/image_matching", exist_ok=True)

    # Create the Flask application
    debug_log("Creating Flask application")
    app = create_app()
    
    # Open browser after a short delay
    if not DEBUG_MODE:  # Don't auto-open browser in debug mode
        Timer(1.5, open_browser).start()
    
    # Run the application with waitress (production server)
    debug_log("Starting server...")
    print("Starting SVT Reproduction Animaux...")
    print("Application running at http://localhost:8080")
    print("Debug mode:", "enabled" if DEBUG_MODE else "disabled")
    print("You can close the application by closing this window")
    
    if DEBUG_MODE:
        # Use Flask's development server in debug mode
        app.run(host='localhost', port=8080, debug=True)
    else:
        # Use waitress in production mode
        serve(app, host='localhost', port=8080)

if __name__ == '__main__':
    main() 