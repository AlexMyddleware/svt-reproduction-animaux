@echo off
title Revijouer - Jeu educatif
echo Lancement de Revijouer...
echo.

:: Activate virtual environment and run the game
call .venv\Scripts\activate.bat
if %ERRORLEVEL% NEQ 0 (
    echo Erreur: L'environnement virtuel n'a pas pu etre active.
    echo Assurez-vous d'avoir execute l'installation comme indique dans le README.
    pause
    exit /b 1
)

:: Run the game
python run.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Une erreur s'est produite lors du lancement du jeu.
    echo.
    pause
    exit /b 1
)

deactivate 