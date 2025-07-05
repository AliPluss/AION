@echo off
REM 🚀 AION Build Script for Windows
REM Alternative to Makefile for Windows systems

echo 🚀 AION Build Script for Windows
echo ================================

if "%1"=="help" goto :help
if "%1"=="test" goto :test
if "%1"=="build" goto :build
if "%1"=="install" goto :install
if "%1"=="clean" goto :clean
if "%1"=="format" goto :format
if "%1"=="lint" goto :lint
if "%1"=="release" goto :release
if "%1"=="github" goto :github
if "%1"=="" goto :help

:help
echo 📋 Available commands:
echo.
echo   build.bat test      - Run tests
echo   build.bat build     - Build package
echo   build.bat install   - Install locally
echo   build.bat clean     - Clean build artifacts
echo   build.bat format    - Format code
echo   build.bat lint      - Run linting
echo   build.bat release   - Build release
echo   build.bat github    - Setup GitHub
echo   build.bat help      - Show this help
echo.
goto :end

:test
echo 🧪 Running tests...
python final_test.py
goto :end

:build
echo 🏗️ Building package...
python build_release.py
goto :end

:install
echo 📦 Installing locally...
python install.py
goto :end

:clean
echo 🧹 Cleaning build artifacts...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist *.egg-info rmdir /s /q *.egg-info
echo ✅ Clean completed
goto :end

:format
echo 🎨 Formatting code...
python -m black . 2>nul || echo ⚠️ black not installed, skipping formatting
goto :end

:lint
echo 🔍 Running linting...
python -m flake8 . 2>nul || echo ⚠️ flake8 not installed, skipping linting
goto :end

:release
echo 🚀 Building release...
python build_release.py
echo ✅ Release built successfully!
echo 📦 Files available in dist/ folder
goto :end

:github
echo 🐙 Setting up GitHub...
python setup_github.py
goto :end

:end
echo.
echo ✅ Command completed!
