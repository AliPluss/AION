@echo off
echo 🔧 Installing AION Development Tools...
echo.

echo 📦 Installing core development dependencies...
python -m pip install --upgrade pip --no-warn-script-location
python -m pip install pytest --no-warn-script-location
python -m pip install flake8 --no-warn-script-location
python -m pip install black --no-warn-script-location
python -m pip install mypy --no-warn-script-location
python -m pip install isort --no-warn-script-location

echo.
echo 📦 Installing additional testing tools...
python -m pip install pytest-mock --no-warn-script-location
python -m pip install pytest-cov --no-warn-script-location
python -m pip install pytest-asyncio --no-warn-script-location

echo.
echo 🧪 Testing installations...
echo ✅ Python version:
python --version

echo ✅ Pip version:
python -m pip --version

echo ✅ Pytest:
python -m pytest --version

echo ✅ Flake8:
python -m flake8 --version

echo ✅ Black:
python -m black --version

echo ✅ MyPy:
python -m mypy --version

echo.
echo 🎉 All development tools installed successfully!
echo 💡 Use 'python -m [tool]' to run tools (e.g., 'python -m pytest')
echo.
pause
