@echo off
setlocal enabledelayedexpansion

:: Change to the script's directory to ensure correct paths
cd /d "%~dp0"

echo ==============================
echo Hospital Queue System - Setup and Launch
echo ==============================

:: Check if Python is available
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python and add it to your PATH.
    pause
    exit /b 1
)
echo Python found in PATH.

:: Handle virtual environment
echo ==============================
echo Setting up Python virtual environment...
echo ==============================

:: Remove existing venv if it exists to ensure clean setup
if exist "venv" (
    echo Removing existing virtual environment...
    rmdir /s /q "venv" 2>nul
)

:: Create new virtual environment
echo Creating new virtual environment...
py -3 -m venv "venv"
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment!
    echo This might be due to issues with the current directory or Python installation.
    echo Try running the script from a different location or check Python installation.
    pause
    exit /b 1
)
echo Virtual environment created successfully!

:: Wait a moment for venv to be fully created
timeout /t 2 /nobreak > nul

:: Verify activate.bat exists
if exist "venv\Scripts\activate.bat" (
    :: Activate using activate.bat
    echo Activating virtual environment...
    call "venv\Scripts\activate.bat"
    if %errorlevel% neq 0 (
        echo ERROR: Failed to activate virtual environment!
        echo This might be due to path issues or incorrect venv creation.
        pause
        exit /b 1
    )
    echo Virtual environment activated!
) else (
    echo activate.bat not found, attempting manual activation...
    :: Manual activation for Linux-style or broken venv
    set "PATH=%~dp0venv\Scripts;%PATH%"
    if exist "venv\Scripts" (
        set "PYTHONPATH=%~dp0venv\Lib\site-packages;%PYTHONPATH%"
        set "VIRTUAL_ENV=%~dp0venv"
    ) else (
        :: Assume Linux-style bin
        set "PATH=%~dp0venv\bin;%PATH%"
        set "PYTHONPATH=%~dp0venv\lib\python*\site-packages;%PYTHONPATH%"
        set "VIRTUAL_ENV=%~dp0venv"
    )
    echo Virtual environment activated manually!
)

:: Upgrade pip
echo ==============================
echo Upgrading pip...
echo ==============================
python -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo WARNING: Failed to upgrade pip, continuing...
)

:: Install Python dependencies
echo ==============================
echo Installing Python dependencies...
echo ==============================
python -m pip install -r "requirements.txt"
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Python dependencies!
    pause
    exit /b 1
)
echo Dependencies installed successfully!

:: Compile C++ backend
echo ==============================
echo Compiling C++ backend...
echo ==============================
if not exist "backend\data_structures.exe" (
    g++ "backend\main.cpp" "backend\data_structures.cpp" "backend\database.cpp" "backend\web.cpp" -o "backend\data_structures.exe" -lsqlite3 -std=c++11
    if %errorlevel% neq 0 (
        echo ERROR: C++ compilation failed!
        echo Make sure g++ (MinGW or similar) is installed and in PATH.
        pause
        exit /b 1
    )
    echo C++ compilation successful!
) else (
    echo C++ executable already exists, skipping compilation...
)

:: Start Python web app
echo ==============================
echo Starting Hospital Queue System Web App...
echo ==============================
start "" python "backend\app_py.py"

:: Wait a few seconds to allow server to start
echo Waiting for server to start...
timeout /t 5 /nobreak > nul

:: Open default browser to localhost
echo Opening browser to http://localhost:5000
start "" "http://localhost:5000"

echo ==============================
echo Setup complete! The app should be running at http://localhost:5000
echo ==============================
pause
