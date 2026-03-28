@echo off
title Sift Installer
color 0A
echo.
echo  ============================================
echo   Sift Installer
echo  ============================================
echo.

:: ── Check Python ─────────────────────────────────────────────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo  [!] Python was not found on your system.
    echo.
    echo  Please install Python 3.10 or later from:
    echo  https://www.python.org/downloads/
    echo.
    echo  IMPORTANT: During installation, tick
    echo  "Add Python to PATH" before clicking Install.
    echo.
    pause
    start https://www.python.org/downloads/
    exit /b 1
)

for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do set PY_VER=%%v
echo  [OK] Python %PY_VER% found.
echo.

:: ── Install location = folder this script is in ──────────────────────────────
set INSTALL_DIR=%~dp0
set INSTALL_DIR=%INSTALL_DIR:~0,-1%
echo  Sift will be installed to:
echo  %INSTALL_DIR%
echo.

:: ── Download from GitHub ──────────────────────────────────────────────────────
echo  Downloading Sift...
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/nimblecloud13/Sift/archive/refs/heads/main.zip' -OutFile '%TEMP%\sift.zip'" 2>nul
if errorlevel 1 (
    echo.
    echo  [!] Download failed. Check your internet connection and try again.
    pause
    exit /b 1
)
echo  [OK] Download complete.
echo.

:: ── Extract ───────────────────────────────────────────────────────────────────
echo  Extracting...
powershell -Command "Expand-Archive -Path '%TEMP%\sift.zip' -DestinationPath '%TEMP%\sift_extracted' -Force"
xcopy /e /y /q "%TEMP%\sift_extracted\Sift-main\*" "%INSTALL_DIR%\" >nul
rmdir /s /q "%TEMP%\sift_extracted" 2>nul
del "%TEMP%\sift.zip" 2>nul
echo  [OK] Extracted to %INSTALL_DIR%
echo.

:: ── Install dependencies ──────────────────────────────────────────────────────
echo  Installing dependencies...
python -m pip install --upgrade pip --quiet
python -m pip install flask pystray pillow --quiet
if errorlevel 1 (
    echo.
    echo  [!] Dependency installation failed.
    echo  Try running this installer as Administrator.
    pause
    exit /b 1
)
echo  [OK] Dependencies installed.
echo.

:: ── Desktop shortcut ─────────────────────────────────────────────────────────
echo  Creating desktop shortcut...
powershell -Command ^
  "$ws = New-Object -ComObject WScript.Shell; ^
   $s = $ws.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\Sift.lnk'); ^
   $s.TargetPath = '%INSTALL_DIR%\run.bat'; ^
   $s.WorkingDirectory = '%INSTALL_DIR%'; ^
   $s.IconLocation = '%INSTALL_DIR%\logo.ico'; ^
   $s.Description = 'Sift Media Sorter'; ^
   $s.Save()"
echo  [OK] Shortcut created on your Desktop.
echo.

:: ── Done ─────────────────────────────────────────────────────────────────────
echo  ============================================
echo   Sift is installed!
echo  ============================================
echo.
echo  Double-click "Sift" on your Desktop to launch.
echo.
set /p LAUNCH= Launch Sift now? (Y/N):
if /i "%LAUNCH%"=="Y" start "" "%INSTALL_DIR%\run.bat"
echo.
pause
