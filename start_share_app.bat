@echo off
start "SHARE App" cmd /k "python C:\Users\rasmu\OneDrive\Skrivebord\Dev\ies-3\src\app.py share_articles.db 1919 SHARE"
start "SHARE Pipeline" cmd /k "python C:\Users\rasmu\OneDrive\Skrivebord\Dev\ies-3\src\pipeline_helper.py share_articles.db SHARE"

start chrome --new-window "http://192.168.86.67:1919/"