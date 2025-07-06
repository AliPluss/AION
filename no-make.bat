@echo off
REM AION No-Make Solution for Windows
REM Completely eliminates make.exe dependency

setlocal enabledelayedexpansion

echo.
echo 🚀 AION No-Make Windows Solution
echo ================================
echo 📍 Zero make.exe dependency
echo.

if "%1"=="" goto help
if /i "%1"=="help" goto help
if /i "%1"=="health-check" goto health-check
if /i "%1"=="test-simple" goto test-simple
if /i "%1"=="install" goto install
if /i "%1"=="quick-start" goto quick-start
if /i "%1"=="setup" goto setup

echo ❌ Unknown command: %1
echo Run 'no-make.bat help' for available commands
goto end

:help
echo.
echo 🤖 AION - No Make Solution
echo ==========================
echo.
echo Available commands:
echo   🔍 health-check - Check system health
echo   ⚡ test-simple  - Run simple tests
echo   📦 install      - Install dependencies
echo   🎯 quick-start  - Start application
echo   ⚙️  setup        - Setup environment
echo   ❓ help         - Show this help
echo.
goto end

:health-check
echo 🔍 Running AION health check...
echo.
python --version
if errorlevel 1 (
    echo ❌ Python not found
    goto error
)

if exist main.py (
    echo ✅ Main application found
) else if exist start_aion_en.py (
    echo ✅ Startup application found  
) else (
    echo ❌ Main application not found
)

if exist requirements.txt (
    echo ✅ Requirements file found
) else (
    echo ❌ Requirements file not found
)

if exist tests (
    echo ✅ Tests directory found
) else (
    echo ❌ Tests directory not found
)

echo.
echo 🎉 Health check completed!
goto end

:test-simple
echo ⚡ Running simple tests...
if exist tests\test_simple.py (
    python -m pytest tests\test_simple.py -v
    if errorlevel 1 (
        echo ❌ Tests failed
        goto error
    ) else (
        echo ✅ Tests passed!
    )
) else (
    echo ❌ Simple tests not found
    goto error
)
goto end

:install
echo 📦 Installing dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Installation failed
    goto error
) else (
    echo ✅ Installation completed!
)
goto end

:quick-start
echo 🎯 Starting AION...
if exist start_aion_en.py (
    python start_aion_en.py
) else if exist main.py (
    python main.py cli
) else (
    echo ❌ No startup file found
    goto error
)
goto end

:setup
echo ⚙️  Setting up environment...
call :install
echo 🎉 Setup completed!
goto end

:error
echo.
echo ❌ Command failed!
exit /b 1

:end
echo.
echo 🎉 Command completed!
exit /b 0
