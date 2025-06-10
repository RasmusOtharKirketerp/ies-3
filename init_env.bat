@echo off
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

IF NOT EXIST requirements.txt (
    echo Creating base requirements.txt...
    echo requests>=2.31.0 > requirements.txt
    echo beautifulsoup4>=4.12.0 >> requirements.txt
    echo pandas>=2.2.0 >> requirements.txt
    echo numpy>=1.26.0 >> requirements.txt
)

echo Installing requirements...
.venv\Scripts\python.exe -m pip install -r requirements.txt
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to install requirements
    exit /b %ERRORLEVEL%
)

REM Do NOT overwrite requirements.txt with pip freeze output


echo Environment setup complete!

REM Open a new terminal and activate .venv
start cmd /k "cd /d C:\Users\rasmu\OneDrive\Skrivebord\Dev\ies-3 && call .venv\Scripts\activate.bat"

REM Start the SHARE app and pipeline
call start_share_app.bat
call start_mette_og_rasmus.bat

ENDLOCAL
