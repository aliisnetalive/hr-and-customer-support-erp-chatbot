@echo off
REM ============================================================================
REM CUSTOMER SUPPORT CHATBOT - STARTUP SCRIPT (Windows)
REM ============================================================================

setlocal enabledelayedexpansion

echo ==================================
echo CUSTOMER SUPPORT CHATBOT - STARTUP
echo ==================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python not found. Install from python.org
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do echo OK %%i
echo.

REM Check .env
if not exist ".env" (
    echo ! No .env file
    if exist ".env.template" (
        echo Creating from template...
        copy .env.template .env >nul
        echo OK Created .env
        echo   Edit it with your PDF filename if different
        echo.
    )
)

REM Check PDF (read from .env or use default)
for /f "tokens=2 delims==" %%i in ('findstr /I "^FILE_PATH=" .env 2^>nul') do set PDF_FILE=%%i
if "!PDF_FILE!"=="" set PDF_FILE=Egyptian_ERP_System_Comprehensive_Manual.pdf

echo Checking PDF: !PDF_FILE!
if not exist "!PDF_FILE!" (
    echo X PDF NOT FOUND: !PDF_FILE!
    echo Please ensure the PDF file exists in this folder
    echo.
    echo If your PDF has a different name, edit .env and change FILE_PATH
    pause
    exit /b 1
)
echo OK PDF found
echo.

REM Check virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo OK venv created
    echo.
)

REM Activate
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing packages...
pip install -r requirements.txt >nul 2>&1
echo OK Dependencies ready
echo.

REM Start
echo ==================================
echo Starting Customer Support Chatbot API
echo ==================================
echo Server: http://localhost:5000
echo Test:   python test_api.py
echo Press Ctrl+C to stop
echo ==================================
echo.

python main_app.py
pause
