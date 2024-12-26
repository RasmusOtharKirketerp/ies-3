:: filepath: /C:/Users/rasmu/OneDrive/Skrivebord/Dev/ies-3/start_app.bat
@echo off
echo Starting the Flask app and daemon processes...

:: Start the Flask app in a new terminal window
start cmd /k "cd /d C:\Users\rasmu\OneDrive\Skrivebord\Dev\ies-3 && .venv\Scripts\activate.bat && python -u .venv/app.py"

:: Start the daemon processes in a new terminal window
start cmd /k "cd /d C:\Users\rasmu\OneDrive\Skrivebord\Dev\ies-3 && .venv\Scripts\activate.bat && python -u .venv/pipeline_helper.py"

:: Open the default web browser and navigate to the Flask app
echo Opening the default browser...
start "" "http://127.0.0.1:5000"

echo All processes started. Check the opened terminals for logs and errors.
pause