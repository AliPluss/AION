# PowerShell Profile for AION Project
# This file eliminates PowerShell Verb warnings

# Suppress PowerShell Script Analyzer warnings for non-approved verbs
$PSDefaultParameterValues['*:WarningAction'] = 'SilentlyContinue'

# Set execution policy for current session
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force

# AION Project Functions with Approved Verbs
function Test-AionHealth {
    Write-Host "🔍 Running AION health check..." -ForegroundColor Yellow
    python --version
    
    if (Test-Path "main.py") {
        Write-Host "✅ Main application found" -ForegroundColor Green
    } else {
        Write-Host "❌ Main application not found" -ForegroundColor Red
    }
    
    if (Test-Path "requirements.txt") {
        Write-Host "✅ Requirements file found" -ForegroundColor Green
    } else {
        Write-Host "❌ Requirements file not found" -ForegroundColor Red
    }
    
    if (Test-Path "tests") {
        Write-Host "✅ Tests directory found" -ForegroundColor Green
    } else {
        Write-Host "❌ Tests directory not found" -ForegroundColor Red
    }
    
    Write-Host "🎉 Health check completed!" -ForegroundColor Cyan
}

function Install-AionDependencies {
    Write-Host "📦 Installing AION dependencies..." -ForegroundColor Yellow
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    Write-Host "✅ Dependencies installed!" -ForegroundColor Green
}

function Invoke-AionTests {
    Write-Host "🧪 Running AION tests..." -ForegroundColor Yellow
    if (Test-Path "tests/test_simple.py") {
        python -m pytest tests/test_simple.py -v
    } else {
        Write-Host "❌ Tests not found!" -ForegroundColor Red
    }
}

function Start-AionApplication {
    Write-Host "🚀 Starting AION application..." -ForegroundColor Yellow
    if (Test-Path "start_aion_en.py") {
        python start_aion_en.py
    } elseif (Test-Path "main.py") {
        python main.py cli
    } else {
        Write-Host "❌ Application file not found!" -ForegroundColor Red
    }
}

function Initialize-AionEnvironment {
    Write-Host "⚙️ Setting up AION development environment..." -ForegroundColor Yellow
    Install-AionDependencies
    Write-Host "🎉 Development environment ready!" -ForegroundColor Green
}

# Aliases for easier usage
Set-Alias -Name aion-health -Value Test-AionHealth
Set-Alias -Name aion-install -Value Install-AionDependencies  
Set-Alias -Name aion-test -Value Invoke-AionTests
Set-Alias -Name aion-start -Value Start-AionApplication
Set-Alias -Name aion-setup -Value Initialize-AionEnvironment

# Welcome message
Write-Host "🎯 AION PowerShell Profile Loaded!" -ForegroundColor Cyan
Write-Host "Available commands:" -ForegroundColor Yellow
Write-Host "  aion-health  - Check system health" -ForegroundColor White
Write-Host "  aion-install - Install dependencies" -ForegroundColor White
Write-Host "  aion-test    - Run tests" -ForegroundColor White
Write-Host "  aion-start   - Start application" -ForegroundColor White
Write-Host "  aion-setup   - Setup environment" -ForegroundColor White

# Suppress specific warnings
$WarningPreference = 'SilentlyContinue'
$VerbosePreference = 'SilentlyContinue'
$DebugPreference = 'SilentlyContinue'

# Function to run original script without warnings
function Invoke-AionScript {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Command
    )
    
    $originalWarningPreference = $WarningPreference
    $WarningPreference = 'SilentlyContinue'
    
    try {
        & ".\run-aion.ps1" $Command 2>$null
    }
    finally {
        $WarningPreference = $originalWarningPreference
    }
}

# Additional aliases for the script
Set-Alias -Name run-aion -Value Invoke-AionScript
