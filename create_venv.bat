@echo off
echo 🔧 Creating AION Virtual Environment...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python first.
    pause
    exit /b 1
)

echo ✅ Python found, creating virtual environment...

REM Remove existing venv if it exists
if exist "aion_env" (
    echo 🗑️ Removing existing virtual environment...
    rmdir /s /q "aion_env"
)

REM Create new virtual environment
echo 📦 Creating new virtual environment...
python -m venv aion_env

REM Check if venv was created successfully
if not exist "aion_env\Scripts\activate.bat" (
    echo ❌ Failed to create virtual environment!
    pause
    exit /b 1
)

echo ✅ Virtual environment created successfully!

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call aion_env\Scripts\activate.bat

REM Upgrade pip first
echo 📦 Upgrading pip...
python -m pip install --upgrade pip

REM Install basic requirements first
echo 📦 Installing basic requirements...
python -m pip install wheel setuptools

REM Check if requirements.txt exists and install
if exist "requirements.txt" (
    echo 📦 Installing from requirements.txt...
    python -m pip install -r requirements.txt
) else (
    echo ⚠️ requirements.txt not found, installing basic packages...
    python -m pip install typer fastapi uvicorn textual rich requests
)

REM Install development requirements if available
if exist "requirements-dev.txt" (
    echo 📦 Installing development requirements...
    python -m pip install -r requirements-dev.txt
) else (
    echo 📦 Installing basic development tools...
    python -m pip install pytest flake8 black mypy
)

echo.
echo 🎉 Virtual environment setup completed!
echo.
echo 💡 To activate the environment manually, run:
echo    aion_env\Scripts\activate.bat
echo.
echo 💡 To deactivate, run:
echo    deactivate
echo.
echo 🧪 Testing installation...
python -c "import sys; print(f'✅ Python: {sys.version}')"
python -c "import pip; print(f'✅ Pip: {pip.__version__}')"

echo.
echo 🎯 Environment is ready for AION development!
pause
