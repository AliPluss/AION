@echo off
echo ========================================
echo    AION Quick Installation Script
echo ========================================
echo.

echo Checking current installations...
echo.

:: Check Node.js
node --version >nul 2>&1
if %errorlevel% == 0 (
    echo [✓] Node.js: Already installed
    for /f "tokens=*" %%i in ('node --version') do echo     Version: %%i
) else (
    echo [✗] Node.js: Not installed
    echo     Download from: https://nodejs.org/en/download
)

echo.

:: Check Rust
rustc --version >nul 2>&1
if %errorlevel% == 0 (
    echo [✓] Rust: Already installed
    for /f "tokens=*" %%i in ('rustc --version') do echo     Version: %%i
) else (
    echo [✗] Rust: Not installed
    echo     Download from: https://rustup.rs/
)

echo.

:: Check C++
g++ --version >nul 2>&1
if %errorlevel% == 0 (
    echo [✓] C++: Already installed
    for /f "tokens=*" %%i in ('g++ --version ^| findstr /C:"g++"') do echo     Version: %%i
) else (
    echo [✗] C++: Not installed
    echo     Download MSYS2 from: https://www.msys2.org/
)

echo.
echo ========================================
echo Installation Instructions:
echo ========================================
echo.
echo 1. Node.js (JavaScript support):
echo    - Go to: https://nodejs.org/en/download
echo    - Download LTS version for Windows
echo    - Run installer with default settings
echo.
echo 2. Rust (High performance):
echo    - Go to: https://rustup.rs/
echo    - Download rustup-init.exe
echo    - Run and choose default installation
echo.
echo 3. C++ (High performance):
echo    - Go to: https://www.msys2.org/
echo    - Download and install MSYS2
echo    - Open MSYS2 terminal and run:
echo      pacman -Syu
echo      pacman -S mingw-w64-x86_64-gcc
echo    - Add C:\msys64\mingw64\bin to PATH
echo.
echo ========================================
echo After installation:
echo ========================================
echo 1. Restart your terminal
echo 2. Run: python main.py start
echo 3. Test all languages in AION
echo.
echo Press any key to exit...
pause >nul
