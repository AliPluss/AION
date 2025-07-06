# AION PowerShell Build Script for Windows
param([string]$Command = "help")

function Show-Help {
    Write-Host "AION - AI Operating Node" -ForegroundColor Cyan
    Write-Host "Available commands:" -ForegroundColor Yellow
    Write-Host "  install      - Install production dependencies" -ForegroundColor Green
    Write-Host "  install-dev  - Install development dependencies" -ForegroundColor Green
    Write-Host "  test         - Run tests" -ForegroundColor Green
    Write-Host "  test-simple  - Run simple tests only" -ForegroundColor Green
    Write-Host "  run-dev      - Run in development mode" -ForegroundColor Green
    Write-Host "  setup        - Setup development environment" -ForegroundColor Green
    Write-Host "  health-check - Check system health" -ForegroundColor Green
    Write-Host "  quick-start  - Quick start AION" -ForegroundColor Green
}

function Install-Dependencies {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    Write-Host "Dependencies installed!" -ForegroundColor Green
}

function Install-DevDependencies {
    Write-Host "Installing dev dependencies..." -ForegroundColor Yellow
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    if (Test-Path "requirements-dev.txt") {
        python -m pip install -r requirements-dev.txt
    }
    Write-Host "Dev dependencies installed!" -ForegroundColor Green
}

function Invoke-AllTests {
    Write-Host "Running tests..." -ForegroundColor Yellow
    if (Test-Path "tests") {
        python -m pytest tests/ -v --tb=short
    } else {
        Write-Host "Tests directory not found!" -ForegroundColor Red
    }
}

function Invoke-SimpleTests {
    Write-Host "Running simple tests..." -ForegroundColor Yellow
    if (Test-Path "tests/test_simple.py") {
        python -m pytest tests/test_simple.py -v
    } else {
        Write-Host "Simple tests not found!" -ForegroundColor Red
    }
}

function Start-Development {
    Write-Host "Starting development mode..." -ForegroundColor Yellow
    if (Test-Path "start_aion_en.py") {
        python start_aion_en.py
    } elseif (Test-Path "main.py") {
        python main.py cli
    } else {
        Write-Host "Main application file not found!" -ForegroundColor Red
    }
}

function Initialize-DevEnvironment {
    Write-Host "Setting up development environment..." -ForegroundColor Yellow
    Install-DevDependencies
    Write-Host "Development environment ready!" -ForegroundColor Green
}

function Test-SystemHealth {
    Write-Host "Running health check..." -ForegroundColor Yellow
    python --version

    if (Test-Path "main.py") {
        Write-Host "Main application found" -ForegroundColor Green
    } else {
        Write-Host "Main application not found" -ForegroundColor Red
    }

    if (Test-Path "requirements.txt") {
        Write-Host "Requirements file found" -ForegroundColor Green
    } else {
        Write-Host "Requirements file not found" -ForegroundColor Red
    }

    if (Test-Path "tests") {
        Write-Host "Tests directory found" -ForegroundColor Green
    } else {
        Write-Host "Tests directory not found" -ForegroundColor Red
    }

    Write-Host "Health check completed!" -ForegroundColor Cyan
}

function Start-Application {
    Write-Host "Quick starting AION..." -ForegroundColor Yellow
    if (Test-Path "start_aion_en.py") {
        python start_aion_en.py
    } else {
        Write-Host "Startup file not found!" -ForegroundColor Red
    }
}

# Command dispatcher
switch ($Command.ToLower()) {
    "help" { Show-Help }
    "install" { Install-Dependencies }
    "install-dev" { Install-DevDependencies }
    "test" { Invoke-AllTests }
    "test-simple" { Invoke-SimpleTests }
    "run-dev" { Start-Development }
    "setup" { Initialize-DevEnvironment }
    "health-check" { Test-SystemHealth }
    "quick-start" { Start-Application }
    default {
        Write-Host "Unknown command: $Command" -ForegroundColor Red
        Write-Host "Run './run-aion.ps1 help' for available commands" -ForegroundColor Yellow
    }
}
