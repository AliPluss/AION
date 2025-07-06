@echo off
REM AION Batch Build Script for Windows
REM Alternative to Makefile for Windows users

if "%1"=="" goto help
if "%1"=="help" goto help
if "%1"=="install" goto install
if "%1"=="install-dev" goto install-dev
if "%1"=="test" goto test
if "%1"=="test-simple" goto test-simple
if "%1"=="lint" goto lint
if "%1"=="format" goto format
if "%1"=="clean" goto clean
if "%1"=="build" goto build
if "%1"=="run-dev" goto run-dev
if "%1"=="setup" goto setup
if "%1"=="health-check" goto health-check
if "%1"=="quick-start" goto quick-start
goto unknown

:help
echo.
echo 🤖 AION - AI Operating Node
echo Available commands:
echo   install      - Install production dependencies
echo   install-dev  - Install development dependencies
echo   test         - Run tests
echo   test-simple  - Run simple tests only
echo   lint         - Run linting
echo   format       - Format code
echo   clean        - Clean build artifacts
echo   build        - Build package
echo   run-dev      - Run in development mode
echo   setup        - Setup development environment
echo   health-check - Check system health
echo   quick-start  - Quick start AION
echo.
goto end

:install
echo 📦 Installing production dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
echo ✅ Production dependencies installed!
goto end

:install-dev
echo 📦 Installing development dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if exist requirements-dev.txt (
    python -m pip install -r requirements-dev.txt
)
echo ✅ Development dependencies installed!
goto end

:test
echo 🧪 Running tests...
if exist tests (
    python -m pytest tests/ -v --tb=short
) else (
    echo ❌ Tests directory not found!
)
goto end

:test-simple
echo 🧪 Running simple tests...
if exist tests\test_simple.py (
    python -m pytest tests/test_simple.py -v
) else (
    echo ❌ Simple tests not found!
)
goto end

:lint
echo 🔍 Running linting...
python -m flake8 . --exclude=venv,aion_env,build,dist
goto end

:format
echo 🎨 Formatting code...
python -m black . --exclude="/(venv|aion_env|build|dist)/"
python -m isort . --skip venv --skip aion_env --skip build --skip dist
goto end

:clean
echo 🧹 Cleaning build artifacts...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
for /d %%i in (*.egg-info) do rmdir /s /q "%%i"
if exist .pytest_cache rmdir /s /q .pytest_cache
if exist .coverage del .coverage
if exist htmlcov rmdir /s /q htmlcov
if exist .mypy_cache rmdir /s /q .mypy_cache
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
del /s /q *.pyc >nul 2>&1
echo ✅ Build artifacts cleaned!
goto end

:build
echo 📦 Building package...
call :clean
python -m build
echo ✅ Package built!
goto end

:run-dev
echo 🚀 Running in development mode...
if exist main.py (
    python main.py cli
) else if exist start_aion_en.py (
    python start_aion_en.py
) else (
    echo ❌ Main application file not found!
)
goto end

:setup
echo ⚙️ Setting up development environment...
call :install-dev
echo ✅ Development environment setup complete!
echo 📝 Don't forget to configure your AI API keys!
goto end

:health-check
echo 🔍 Running AION health check...
python -c "import sys; print(f'✅ Python version: {sys.version}')"

if exist main.py (
    echo ✅ Main application found
) else if exist aion_project\main.py (
    echo ✅ Main application found
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

echo 🎉 Health check completed!
goto end

:quick-start
echo 🚀 Quick starting AION...
if exist start_aion_en.py (
    python start_aion_en.py
) else if exist main.py (
    python main.py
) else (
    echo ❌ Startup file not found!
)
goto end

:unknown
echo ❌ Unknown command: %1
echo Run 'make.bat help' to see available commands
goto end

:end
