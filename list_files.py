import os

def list_project_files():
    """List all project files excluding cache, build, and virtual environment files."""
    excluded_dirs = [
        '.git', 
        '__pycache__', 
        '.pytest_cache', 
        'htmlcov', 
        'build', 
        'dist', 
        '.venv'
    ]
    excluded_extensions = ('.pyc', '.pyo', '.pyd')

    for root, dirs, files in os.walk('.'):
        # Skip excluded directories
        if any(x in root for x in excluded_dirs):
            continue
            
        for file in files:
            if not file.endswith(excluded_extensions):
                print(os.path.join(root, file))

if __name__ == '__main__':
    list_project_files() 