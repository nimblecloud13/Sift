@echo off
title Sift
cd /d "%~dp0"

echo.
echo  Sift
echo  ─────────────────────────────────────
echo.

python -c "import flask" 2>nul
if errorlevel 1 (
    echo  Flask not found. Installing...
    python -m pip install flask
    echo.
)

python -c "import pystray, PIL" 2>nul
if errorlevel 1 (
    echo  Installing tray dependencies...
    python -m pip install pystray pillow
    echo.
)

echo  Starting Sift...
echo  It will appear in your system tray and taskbar.
echo  (browser will open automatically)
echo.

start "" pythonw server.py
