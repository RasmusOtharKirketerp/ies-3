@echo off
REM Activate the virtual environment in each started command window

start "SHARE App" cmd /k "call C:\Users\rasmu\OneDrive\Skrivebord\Dev\ies-3\.venv\Scripts\activate.bat && python C:\Users\rasmu\OneDrive\Skrivebord\Dev\ies-3\src\app.py share_articles.db 1919 SHARE"
start "SHARE Pipeline" cmd /k "call C:\Users\rasmu\OneDrive\Skrivebord\Dev\ies-3\.venv\Scripts\activate.bat && python C:\Users\rasmu\OneDrive\Skrivebord\Dev\ies-3\src\pipeline_helper.py share_articles.db SHARE"

start chrome --new-window "http://192.168.86.43:1919/"