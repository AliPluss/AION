# Simple AION Requirements Installation Script
Write-Host "AION Requirements Installation" -ForegroundColor Cyan
Write-Host "==============================" -ForegroundColor Cyan

# Function to check if a command exists
function Test-Command($cmdname) {
    return [bool](Get-Command -Name $cmdname -ErrorAction SilentlyContinue)
}

# Check current status
Write-Host "`nChecking current installations..." -ForegroundColor Yellow

Write-Host "Python: " -NoNewline
if (Test-Command python) {
    Write-Host "Available" -ForegroundColor Green
    python --version
} else {
    Write-Host "Not found" -ForegroundColor Red
}

Write-Host "Node.js: " -NoNewline
if (Test-Command node) {
    Write-Host "Available" -ForegroundColor Green
    node --version
} else {
    Write-Host "Not found - Will install" -ForegroundColor Yellow
}

Write-Host "Rust: " -NoNewline
if (Test-Command rustc) {
    Write-Host "Available" -ForegroundColor Green
    rustc --version
} else {
    Write-Host "Not found - Will install" -ForegroundColor Yellow
}

Write-Host "C++: " -NoNewline
if (Test-Command g++) {
    Write-Host "Available" -ForegroundColor Green
    g++ --version | Select-Object -First 1
} else {
    Write-Host "Not found - Will install" -ForegroundColor Yellow
}

# Check if Chocolatey is available
Write-Host "`nChecking Chocolatey..." -ForegroundColor Yellow
if (-not (Test-Command choco)) {
    Write-Host "Installing Chocolatey..." -ForegroundColor Green
    try {
        Set-ExecutionPolicy Bypass -Scope Process -Force
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
        iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
        Write-Host "Chocolatey installed successfully" -ForegroundColor Green
    } catch {
        Write-Host "Failed to install Chocolatey: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "Please install manually from https://chocolatey.org/" -ForegroundColor Yellow
        Read-Host "Press Enter to continue"
        exit 1
    }
} else {
    Write-Host "Chocolatey is available" -ForegroundColor Green
}

# Install Node.js
if (-not (Test-Command node)) {
    Write-Host "`nInstalling Node.js..." -ForegroundColor Yellow
    try {
        choco install nodejs -y
        Write-Host "Node.js installed successfully" -ForegroundColor Green
    } catch {
        Write-Host "Failed to install Node.js" -ForegroundColor Red
    }
}

# Install Rust
if (-not (Test-Command rustc)) {
    Write-Host "`nInstalling Rust..." -ForegroundColor Yellow
    try {
        $rustupUrl = "https://win.rustup.rs/x86_64"
        $rustupPath = "$env:TEMP\rustup-init.exe"
        
        Write-Host "Downloading Rust installer..." -ForegroundColor Cyan
        Invoke-WebRequest -Uri $rustupUrl -OutFile $rustupPath
        
        Write-Host "Installing Rust..." -ForegroundColor Cyan
        Start-Process -FilePath $rustupPath -ArgumentList "-y" -Wait
        
        Write-Host "Rust installed successfully" -ForegroundColor Green
    } catch {
        Write-Host "Failed to install Rust: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Install MinGW-w64
if (-not (Test-Command g++)) {
    Write-Host "`nInstalling MinGW-w64..." -ForegroundColor Yellow
    try {
        choco install mingw -y
        Write-Host "MinGW-w64 installed successfully" -ForegroundColor Green
    } catch {
        Write-Host "Failed to install MinGW-w64" -ForegroundColor Red
    }
}

Write-Host "`nInstallation completed!" -ForegroundColor Green
Write-Host "Please restart your terminal to refresh PATH variables" -ForegroundColor Yellow
Read-Host "Press Enter to exit"
