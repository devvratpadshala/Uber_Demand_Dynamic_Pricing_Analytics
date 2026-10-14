@echo off
REM =========================================================================
REM GitHub Upload Script: Uber Demand and Dynamic Pricing Analytics
REM =========================================================================

echo.
echo =========================================================================
echo   UBER DEMAND AND DYNAMIC PRICING ANALYTICS - GITHUB UPLOADER
echo =========================================================================
echo.

cd /d "%~dp0"

echo [INFO] Staging all files...
git add .

echo [INFO] Committing latest changes...
git commit -m "Update project files and documentation" 2>nul || echo [INFO] Working tree clean, no new changes to commit.

echo.
echo [INFO] Current remote origin:
git remote -v

echo.
echo =========================================================================
echo [IMPORTANT] Ensure you have created an empty repository on GitHub named:
echo             Uber_Demand_Dynamic_Pricing_Analytics
echo             under your GitHub account (Devvrat26):
echo             https://github.com/new
echo =========================================================================
echo.
pause

echo [INFO] Pushing code to GitHub branch main...
git push -u origin main

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Git push failed.
    echo Common reasons:
    echo 1. The repository 'Uber_Demand_Dynamic_Pricing_Analytics' is not yet created on GitHub.
    echo    Create it at: https://github.com/new (do NOT check Initialize with README).
    echo 2. Authentication required: Log in when the Git Credential Manager prompt appears.
    echo.
) else (
    echo.
    echo =========================================================================
    echo [SUCCESS] Project successfully uploaded to GitHub!
    echo URL: https://github.com/Devvrat26/Uber_Demand_Dynamic_Pricing_Analytics
    echo =========================================================================
    echo.
)

pause
