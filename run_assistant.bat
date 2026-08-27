@echo off
echo Mengaktifkan AI Assistant...
cd /d "%~dp0"
call .\.venv\Scripts\activate.bat
python ai_assistant.py
pause
