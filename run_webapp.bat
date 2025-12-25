@echo off
cd /d "%~dp0"
echo Compiling C++ backend...

:: Compile C++ backend
g++ backend/main.cpp backend/data_structures.cpp backend/database.cpp backend/web.cpp -o backend/ds.exe -lsqlite3 -std=c++11
if %errorlevel% neq 0 (
    echo Compilation failed!
    pause
    exit /b 1
)
echo Compilation successful!

:: Start Python web app
echo Starting Hospital Queue System Web App...
start "" python backend/app_py.py

:: Wait a few seconds to allow server to start
timeout /t 3 /nobreak > nul

:: Open default browser to localhost
start "" http://localhost:5000
