@echo off
REM AION - AI Operating Node Windows Launcher
REM Quick launcher for Windows systems

setlocal enabledelayedexpansion

echo.
echo 🤖 AION - AI Operating Node
echo ============================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.10 or higher from https://python.org
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo 🐍 Python version: %PYTHON_VERSION%

REM Get the directory where this batch file is located
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM Parse command line arguments
set COMMAND=%1
if "%COMMAND%"=="" set COMMAND=run

if "%COMMAND%"=="help" (
    echo.
    echo Usage: aion.bat [command]
    echo.
    echo Commands:
    echo   setup     - Setup AION ^(create directories, install dependencies^)
    echo   install   - Install dependencies only
    echo   config    - Setup configuration files
    echo   run       - Run AION ^(default^)
    echo   web       - Start web interface
    echo   help      - Show this help
    echo.
    echo Examples:
    echo   aion.bat setup    # First time setup
    echo   aion.bat          # Run AION
    echo   aion.bat web      # Start web interface
    echo.
    pause
    exit /b 0
)

if "%COMMAND%"=="setup" (
    echo 🔧 Setting up AION...
    python run.py setup
    if errorlevel 1 (
        echo ❌ Setup failed
        pause
        exit /b 1
    )
    echo ✅ Setup completed successfully!
    echo.
    echo 📝 Next steps:
    echo 1. Edit ~/.aion/config/ai_config.json to add your API keys
    echo 2. Run 'aion.bat' to start AION
    echo.
    pause
    exit /b 0
)

if "%COMMAND%"=="install" (
    echo 📦 Installing dependencies...
    python run.py install
    if errorlevel 1 (
        echo ❌ Installation failed
        pause
        exit /b 1
    )
    echo ✅ Dependencies installed successfully!
    pause
    exit /b 0
)

if "%COMMAND%"=="config" (
    echo 📋 Setting up configuration...
    python run.py config
    echo ✅ Configuration setup completed!
    pause
    exit /b 0
)

if "%COMMAND%"=="web" (
    echo 🌐 Starting AION Web Interface...
    python -c "
import sys
sys.path.append('.')
from interfaces.web import WebInterface
from utils.translator import Translator

translator = Translator()
web = WebInterface(translator)
web.start()
"
    if errorlevel 1 (
        echo ❌ Failed to start web interface
        pause
        exit /b 1
    )
    exit /b 0
)

if "%COMMAND%"=="run" (
    echo 🚀 Starting AION...
    
    REM Check if main.py exists
    if not exist "main.py" (
        echo ❌ main.py not found
        echo Please make sure you're in the AION directory
        pause
        exit /b 1
    )
    
    REM Run AION
    python main.py
    if errorlevel 1 (
        echo ❌ AION exited with error
        pause
        exit /b 1
    )
    exit /b 0
)

REM Unknown command
echo ❌ Unknown command: %COMMAND%
echo Run 'aion.bat help' for available commands
pause
exit /b 1
