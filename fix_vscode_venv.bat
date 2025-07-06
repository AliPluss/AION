@echo off
echo 🔧 Fixing VS Code Virtual Environment Issue...
echo.

REM Step 1: Clean up any existing problematic venv
echo 🧹 Cleaning up existing environments...
if exist ".venv" rmdir /s /q ".venv"
if exist "venv" rmdir /s /q "venv"
if exist "aion_env" rmdir /s /q "aion_env"

REM Step 2: Create fresh virtual environment
echo 📦 Creating fresh virtual environment...
python -m venv .venv

REM Step 3: Activate and upgrade pip
echo 🔄 Activating environment and upgrading pip...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip wheel setuptools

REM Step 4: Install minimal requirements first
echo 📦 Installing minimal requirements...
if exist "requirements-minimal.txt" (
    python -m pip install -r requirements-minimal.txt
) else (
    echo 📦 Installing core packages...
    python -m pip install typer rich colorama fastapi uvicorn requests pydantic python-dotenv
)

REM Step 5: Try to install full requirements (with error handling)
if exist "requirements.txt" (
    echo 📦 Attempting to install full requirements...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo ⚠️ Some packages failed to install, but core functionality should work
    ) else (
        echo ✅ All requirements installed successfully!
    )
)

REM Step 6: Install development tools
echo 📦 Installing development tools...
python -m pip install pytest flake8 black mypy

REM Step 7: Create VS Code settings
echo 🔧 Creating VS Code settings...
if not exist ".vscode" mkdir ".vscode"

echo { > .vscode\settings.json
echo   "python.defaultInterpreterPath": "./.venv/Scripts/python.exe", >> .vscode\settings.json
echo   "python.terminal.activateEnvironment": true, >> .vscode\settings.json
echo   "python.testing.pytestEnabled": true, >> .vscode\settings.json
echo   "python.testing.pytestArgs": ["tests"], >> .vscode\settings.json
echo   "python.linting.enabled": true, >> .vscode\settings.json
echo   "python.linting.flake8Enabled": true, >> .vscode\settings.json
echo   "python.formatting.provider": "black" >> .vscode\settings.json
echo } >> .vscode\settings.json

echo ✅ VS Code settings created!

REM Step 8: Test the environment
echo 🧪 Testing the environment...
python -c "import sys; print(f'✅ Python: {sys.version}')"
python -c "import typer; print('✅ Typer imported successfully')"
python -c "import rich; print('✅ Rich imported successfully')"

echo.
echo 🎉 VS Code Virtual Environment fixed!
echo.
echo 💡 Next steps:
echo 1. Restart VS Code
echo 2. Press Ctrl+Shift+P and select "Python: Select Interpreter"
echo 3. Choose the interpreter from .venv folder
echo.
echo 🎯 Environment is ready for development!
pause
