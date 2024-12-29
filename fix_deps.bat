@echo off
echo Fixing dependencies...

python -m pip uninstall -y googletrans httpcore httpx
python -m pip install googletrans==4.0.0rc1
python -m pip install httpcore>=0.9.1,<0.10.0
python -m pip install httpx>=0.13.3,<0.14.0

echo Dependencies fixed! You can now run start_app.bat again.
pause
