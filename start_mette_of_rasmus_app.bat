@echo off
start cmd /k "python C:\Users\rasmu\OneDrive\Skrivebord\Dev\ies-3\src\app.py rasmus_articles.db 1910 Rasmus"
start cmd /k "python C:\Users\rasmu\OneDrive\Skrivebord\Dev\ies-3\src\pipeline_helper.py rasmus_articles.db Rasmus"

start chrome --new-window "http://192.168.86.67:1910/" "http://192.168.86.67:1910/status"

start cmd /k "python C:\Users\rasmu\OneDrive\Skrivebord\Dev\ies-3\src\app.py mette_articles.db 1911 Mette"
start cmd /k "python C:\Users\rasmu\OneDrive\Skrivebord\Dev\ies-3\src\pipeline_helper.py mette_articles.db Mette"

start chrome --new-window "http://192.168.86.67:1911/" "http://192.168.86.67:1911/status"