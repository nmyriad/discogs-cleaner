@echo off
setlocal

echo.
echo  discogs-cleaner — setup
echo  ========================
echo.

:: Check for Python
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo  [OK] Python is already installed.
    python --version
    goto :start_server
)

:: Try py launcher too
py --version >nul 2>&1
if %errorlevel% == 0 (
    echo  [OK] Python is already installed (via py launcher).
    py --version
    goto :start_server_py
)

:: Python not found — install via winget
echo  [..] Python not found. Installing via winget...
echo.

winget --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  [!!] winget not found. Please install Python manually:
    echo       https://www.python.org/downloads/
    echo       Make sure to check "Add Python to PATH" during install.
    pause
    exit /b 1
)

winget install Python.Python.3.12 --silent --accept-package-agreements --accept-source-agreements
if %errorlevel% neq 0 (
    echo.
    echo  [!!] winget install failed. Please install Python manually:
    echo       https://www.python.org/downloads/
    pause
    exit /b 1
)

echo.
echo  [OK] Python installed successfully.
echo  [!!] Please close and reopen this window, then run setup.bat again.
echo       (Windows needs a fresh shell to pick up the new PATH.)
pause
exit /b 0

:start_server
echo.
echo  [OK] Starting discogs-cleaner server at http://localhost:7842
echo       Press Ctrl+C to stop.
echo.
python server.py
goto :end

:start_server_py
echo.
echo  [OK] Starting discogs-cleaner server at http://localhost:7842
echo       Press Ctrl+C to stop.
echo.
py server.py
goto :end

:end
endlocal
