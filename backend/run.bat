@echo off
REM Contract Analyzer Backend - Quick Start Script (Windows)

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║     Contract Analyzer - Backend Setup ^& Run                ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Check Python version
echo ▶ Checking Python version...
python --version
if errorlevel 1 (
    echo ✗ Python not found. Please install Python 3.8+
    pause
    exit /b 1
)
echo ✓ Python found
echo.

REM Create virtual environment
if not exist "venv" (
    echo ▶ Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ✗ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)
echo.

REM Activate virtual environment
echo ▶ Activating virtual environment...
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated
echo.

REM Install dependencies
echo ▶ Installing dependencies...
pip install --upgrade pip >nul 2>&1
pip install -q -r requirements.txt
if errorlevel 1 (
    echo ✗ Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed
echo.

REM Download spaCy model
echo ▶ Downloading spaCy English model...
python -m spacy download en_core_web_sm
if errorlevel 1 (
    echo ⚠ Warning: spaCy model download may have failed
    echo   You can try again with: python -m spacy download en_core_web_sm
)
echo ✓ spaCy setup attempted
echo.

REM Create directories
echo ▶ Creating necessary directories...
if not exist "uploads" mkdir uploads
echo ✓ Directories created
echo.

REM Create .env if not exists
if not exist ".env" (
    echo ▶ Creating .env from template...
    copy .env.example .env
    echo ✓ .env created (review and update if needed)
) else (
    echo ✓ .env already exists
)
echo.

echo ╔════════════════════════════════════════════════════════════╗
echo ║              Setup Complete! ✓                             ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo Next: Start the backend with:
echo   python -m app.main
echo.
echo API will be available at: http://localhost:8000
echo Documentation: http://localhost:8000/docs
echo.
pause
