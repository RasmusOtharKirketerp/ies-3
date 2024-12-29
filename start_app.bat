@echo off
start cmd /k "python C:\Users\rasmu\OneDrive\Skrivebord\Dev\ies-3\src\app.py"
start cmd /k "python C:\Users\rasmu\OneDrive\Skrivebord\Dev\ies-3\src\pipeline_helper.py"

start chrome http://localhost:5000/
start chrome http://localhost:5000/status
