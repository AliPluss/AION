# AION Requirements Installation Script for Windows
# تثبيت متطلبات AION على نظام Windows

Write-Host "🚀 AION Requirements Installation Script" -ForegroundColor Cyan
Write-Host "سكريبت تثبيت متطلبات AION" -ForegroundColor Cyan
Write-Host "=" * 50

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if (-not $isAdmin) {
    Write-Host "Warning: This script should be run as Administrator" -ForegroundColor Yellow
    Write-Host "This script will continue but some installations may fail" -ForegroundColor Yellow
    Read-Host "Press Enter to continue"
}

# Function to check if a command exists
function Test-Command($cmdname) {
    return [bool](Get-Command -Name $cmdname -ErrorAction SilentlyContinue)
}

# Check and install Chocolatey (package manager for Windows)
Write-Host "🍫 Checking Chocolatey..." -ForegroundColor Yellow
if (-not (Test-Command choco)) {
    Write-Host "📦 Installing Chocolatey..." -ForegroundColor Green
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    refreshenv
} else {
    Write-Host "✅ Chocolatey already installed" -ForegroundColor Green
}

# Install Node.js
Write-Host "`n🟨 Installing Node.js..." -ForegroundColor Yellow
if (-not (Test-Command node)) {
    choco install nodejs -y
    Write-Host "✅ Node.js installed successfully" -ForegroundColor Green
} else {
    Write-Host "✅ Node.js already installed" -ForegroundColor Green
    node --version
}

# Install Rust
Write-Host "`n🦀 Installing Rust..." -ForegroundColor Yellow
if (-not (Test-Command rustc)) {
    # Download and install Rust
    $rustupUrl = "https://win.rustup.rs/x86_64"
    $rustupPath = "$env:TEMP\rustup-init.exe"
    
    Write-Host "📥 Downloading Rust installer..." -ForegroundColor Cyan
    Invoke-WebRequest -Uri $rustupUrl -OutFile $rustupPath
    
    Write-Host "🔧 Installing Rust..." -ForegroundColor Cyan
    Start-Process -FilePath $rustupPath -ArgumentList "-y" -Wait
    
    # Add Rust to PATH for current session
    $env:PATH += ";$env:USERPROFILE\.cargo\bin"
    
    Write-Host "✅ Rust installed successfully" -ForegroundColor Green
} else {
    Write-Host "✅ Rust already installed" -ForegroundColor Green
    rustc --version
}

# Install MinGW-w64 (C++ compiler)
Write-Host "`n⚡ Installing MinGW-w64 (C++ compiler)..." -ForegroundColor Yellow
if (-not (Test-Command g++)) {
    choco install mingw -y
    Write-Host "✅ MinGW-w64 installed successfully" -ForegroundColor Green
} else {
    Write-Host "✅ MinGW-w64 already installed" -ForegroundColor Green
    g++ --version
}

# Refresh environment variables
Write-Host "`n🔄 Refreshing environment variables..." -ForegroundColor Yellow
refreshenv

# Final verification
Write-Host "`n🔍 Final Verification:" -ForegroundColor Cyan
Write-Host "=" * 30

Write-Host "Python: " -NoNewline
if (Test-Command python) {
    Write-Host "✅ Available" -ForegroundColor Green
    python --version
} else {
    Write-Host "❌ Not found" -ForegroundColor Red
}

Write-Host "Node.js: " -NoNewline
if (Test-Command node) {
    Write-Host "✅ Available" -ForegroundColor Green
    node --version
} else {
    Write-Host "❌ Not found" -ForegroundColor Red
}

Write-Host "Rust: " -NoNewline
if (Test-Command rustc) {
    Write-Host "✅ Available" -ForegroundColor Green
    rustc --version
} else {
    Write-Host "❌ Not found" -ForegroundColor Red
}

Write-Host "C++: " -NoNewline
if (Test-Command g++) {
    Write-Host "✅ Available" -ForegroundColor Green
    g++ --version | Select-Object -First 1
} else {
    Write-Host "❌ Not found" -ForegroundColor Red
}

Write-Host "`n🎉 Installation completed!" -ForegroundColor Green
Write-Host "Installation finished!" -ForegroundColor Green
Write-Host "`n📝 Note: You may need to restart your terminal or computer for all changes to take effect."
Write-Host "Note: Restart terminal or computer for changes to take effect."

Read-Host "`nPress Enter to exit"
