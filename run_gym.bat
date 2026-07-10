@echo off
title Muscle Fit Gym Server Launchpad
echo ==========================================
echo Starting Muscle Fit Gym Server...
echo ==========================================
echo.

:: Open browser automatically
start "" "http://127.0.0.1:8000/"

:: Start Django development server
call venv\Scripts\python.exe manage.py runserver

pause
