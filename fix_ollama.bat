@echo off
echo Fixing ollama dependencies...

REM Uninstall conflicting packages
python -m pip uninstall -y ollama httpx

REM Install specific working versions
python -m pip install httpx==0.24.1
python -m pip install ollama==0.1.6

echo Dependencies fixed! You can now run start_app.bat again.
pause
