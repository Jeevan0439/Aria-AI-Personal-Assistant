@echo off
title Aria - Your Personal AI Assistant
echo ========================================
echo    Starting Aria - Your AI Assistant
echo ========================================
echo.

echo Starting Ollama...
start /min "" ollama serve
timeout /t 3 /nobreak >nul

echo Loading Mistral model...
start /min "" ollama run mistral
timeout /t 5 /nobreak >nul

echo Launching Aria...
cd /d "F:\Aria"
py -3.11 main.py

pause