# Set window title
$host.UI.RawUI.WindowTitle = "Revijouer - Jeu educatif"

# Function to show a message in color
function Write-ColorMessage {
    param([string]$Message, [string]$Color = "White")
    Write-Host $Message -ForegroundColor $Color
}

Write-ColorMessage "Lancement de Revijouer..." "Cyan"
Write-ColorMessage "=============================" "Cyan"
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path ".venv\Scripts\Activate.ps1")) {
    Write-ColorMessage "Erreur: L'environnement virtuel n'existe pas." "Red"
    Write-ColorMessage "Veuillez suivre les instructions d'installation dans le README." "Yellow"
    Write-Host ""
    Read-Host "Appuyez sur Entree pour fermer"
    exit 1
}

try {
    # Activate virtual environment
    & .venv\Scripts\Activate.ps1

    # Set debug mode for better error reporting
    $env:SVT_DEBUG = 1

    # Run the application
    python run.py

    # Deactivate virtual environment
    deactivate
}
catch {
    Write-ColorMessage "Une erreur s'est produite:" "Red"
    Write-ColorMessage $_.Exception.Message "Red"
    Write-Host ""
    Read-Host "Appuyez sur Entree pour fermer"
    exit 1
} 