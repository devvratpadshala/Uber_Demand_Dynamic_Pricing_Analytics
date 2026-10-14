@echo off
REM =========================================================================
REM Launcher Script: Uber Demand and Dynamic Pricing Analytics
REM Subject: Business Analytics and Visualization (BAV) - CVM University
REM =========================================================================

echo.
echo =========================================================================
echo   UBER DEMAND AND DYNAMIC PRICING ANALYTICS - LAUNCHER
echo =========================================================================
echo.

cd /d "%~dp0"

set "PYTHON_EXE=python"
if exist ".venv\Scripts\python.exe" (
    echo [INFO] Activating project virtual environment .venv
    call .venv\Scripts\activate.bat
    set "PYTHON_EXE=.venv\Scripts\python.exe"
) else (
    echo [INFO] Using system Python interpreter
)

echo [INFO] Launching Streamlit Interactive Dashboard...
echo [INFO] Access the web UI at: http://localhost:8501
echo [INFO] Press Ctrl+C in this terminal window to stop the application.
echo.

%PYTHON_EXE% -m streamlit run app.py --server.headless=false --browser.serverAddress="localhost"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] The application exited with an error.
    pause
)
