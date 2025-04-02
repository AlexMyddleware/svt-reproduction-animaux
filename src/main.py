import os
import webbrowser
from threading import Timer
from waitress import serve
from svt_app import create_app

def open_browser() -> None:
    """Open the default web browser to the application URL."""
    webbrowser.open('http://localhost:8080')

def main() -> None:
    """
    Main entry point for the application.
    Sets up the production server and launches the browser.
    """
    # Ensure the data directories exist
    os.makedirs("assets/Data/fill_the_blanks", exist_ok=True)
    os.makedirs("assets/Data/image_matching", exist_ok=True)

    # Create the Flask application
    app = create_app()
    
    # Open browser after a short delay
    Timer(1.5, open_browser).start()
    
    # Run the application with waitress (production server)
    print("Starting Révijouer...")
    print("Application running at http://localhost:8080")
    print("You can close the application by closing this window")
    serve(app, host='localhost', port=8080)

if __name__ == '__main__':
    main() 