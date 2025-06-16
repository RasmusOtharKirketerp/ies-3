@echo off

REM init_env.bat
REM This script sets up a Python virtual environment, installs dependencies, and starts the SHARE app and pipeline.
REM It also opens a new terminal window with the virtual environment activated.

SETLOCAL

echo Checking Python installation...
python --version
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to find Python! Please install Python 3.x
    exit /b %ERRORLEVEL%
)

echo Creating Python virtual environment...
python -m venv .venv
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to create virtual environment
    exit /b %ERRORLEVEL%
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to activate virtual environment
    exit /b %ERRORLEVEL%
)

echo Ensuring pip is installed...
.venv\Scripts\python.exe -m ensurepip --default-pip
IF %ERRORLEVEL% NEQ 0 (
    echo Warning: Could not ensure pip installation
)

echo Upgrading pip...
.venv\Scripts\python.exe -m pip install --upgrade pip
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to upgrade pip
    exit /b %ERRORLEVEL%
)

echo Installing requirements...
.venv\Scripts\python.exe -m pip install -r requirements.txt
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to install requirements
    exit /b %ERRORLEVEL%
)

REM Download NLTK punkt data
echo Downloading NLTK punkt data...
.venv\Scripts\python.exe -c "import nltk; nltk.download('punkt')"

REM Do NOT overwrite requirements.txt with pip freeze output


echo Environment setup complete!

REM Open a new terminal and activate .venv
start cmd /k "cd /d C:\Users\rasmu\OneDrive\Skrivebord\Dev\ies-3 && call .venv\Scripts\activate.bat"

REM Start the SHARE app and pipeline in a new terminal
start cmd /k "cd /d C:\Users\rasmu\OneDrive\Skrivebord\Dev\ies-3 && call start_share_app.bat"

REM Start the METTE OG RASMUS app in a new terminal
start cmd /k "cd /d C:\Users\rasmu\OneDrive\Skrivebord\Dev\ies-3 && call start_mette_og_rasmus_app.bat"

ENDLOCAL
