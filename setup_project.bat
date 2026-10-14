@echo off
REM =========================================================================
REM Setup Script: Uber Demand and Dynamic Pricing Analytics
REM Subject: Business Analytics and Visualization (BAV) - CVM University
REM =========================================================================

echo.
echo =========================================================================
echo   UBER DEMAND AND DYNAMIC PRICING ANALYTICS - ENVIRONMENT SETUP
echo =========================================================================
echo.

cd /d "%~dp0"

REM 1. Check Python installation
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed or not available in the system PATH.
    echo Please install Python 3.10+ and re-run this setup script.
    pause
    exit /b 1
)

echo [INFO] Python detected:
python --version
echo.

REM 2. Create virtual environment (.venv) if not already created
if not exist ".venv" (
    echo [INFO] Creating local virtual environment in .venv ...
    python -m venv .venv
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo [SUCCESS] Virtual environment created successfully.
) else (
    echo [INFO] Virtual environment .venv already exists.
)

REM 3. Activate virtual environment
call .venv\Scripts\activate.bat
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Could not activate virtual environment.
    pause
    exit /b 1
)

echo [INFO] Upgrading pip...
python -m pip install --upgrade pip --quiet

echo [INFO] Installing required dependencies from requirements.txt...
python -m pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Dependency installation encountered an issue.
    pause
    exit /b 1
)

echo.
echo =========================================================================
echo [SUCCESS] Environment setup is complete!
echo You can now launch the dashboard by double-clicking 'run_project.bat'.
echo =========================================================================
echo.
pause
