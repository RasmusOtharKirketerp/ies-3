@echo off
echo Closing all Rasmus and Mette app and pipeline processes...

REM Kill all python processes (will terminate app.py and pipeline_helper.py)
taskkill /F /IM python.exe >nul 2>&1

REM Kill all cmd.exe windows (will close all open Command Prompt windows)
taskkill /F /IM cmd.exe >nul 2>&1

REM Kill all old SHARE app and pipeline processes in chrome
taskkill /F /IM chrome.exe