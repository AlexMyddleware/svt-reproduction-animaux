import os
import subprocess
from flask import Blueprint, jsonify, request

game_routes = Blueprint('game_routes', __name__)

@game_routes.route('/game/open_folder', methods=['POST'])
def open_folder():
    """Open a folder in the system's file explorer."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'Invalid JSON data'}), 400
            
        folder_path = data.get('path', '')
        
        # Get the base directory (where the questions are stored)
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'assets', 'Data', 'fill_the_blanks'))
        
        # Join with the requested folder path
        abs_path = os.path.abspath(os.path.join(base_dir, folder_path))
        
        # Security check - make sure the path is within the base directory
        if not abs_path.startswith(base_dir):
            return jsonify({'success': False, 'message': 'Invalid folder path'}), 403
            
        # Check if the folder exists
        if not os.path.exists(abs_path):
            return jsonify({'success': False, 'message': 'Folder not found'}), 404
            
        if os.name == 'nt':  # Windows
            os.startfile(abs_path)
        elif os.name == 'posix':  # macOS and Linux
            if os.path.exists('/usr/bin/xdg-open'):  # Linux
                subprocess.run(['xdg-open', abs_path])
            else:  # macOS
                subprocess.run(['open', abs_path])
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500 