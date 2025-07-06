# PowerShell Installation Script for AION Dependencies
# Enhanced version with better error handling and user guidance

Write-Host "=== AION Dependencies Installation ===" -ForegroundColor Cyan
Write-Host "Installing Node.js, Rust, and MinGW-w64..." -ForegroundColor Yellow

# Function to test if a command exists
function Test-Command($cmdname) {
    return [bool](Get-Command -Name $cmdname -ErrorAction SilentlyContinue)
}

# Function to check if running as administrator
function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Function to download and install Node.js
function Install-NodeJS {
    Write-Host "Downloading Node.js LTS..." -ForegroundColor Yellow
    $nodeUrl = "https://nodejs.org/dist/v20.10.0/node-v20.10.0-x64.msi"
    $nodeInstaller = "$env:TEMP\nodejs-installer.msi"
    
    try {
        Invoke-WebRequest -Uri $nodeUrl -OutFile $nodeInstaller -UseBasicParsing
        Write-Host "Installing Node.js..." -ForegroundColor Yellow
        Start-Process msiexec.exe -Wait -ArgumentList "/i $nodeInstaller /quiet /norestart"
        Remove-Item $nodeInstaller -Force
        Write-Host "Node.js installation completed!" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "Failed to install Node.js: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Function to download and install Rust
function Install-Rust {
    Write-Host "Downloading Rust installer..." -ForegroundColor Yellow
    $rustUrl = "https://static.rust-lang.org/rustup/dist/x86_64-pc-windows-msvc/rustup-init.exe"
    $rustInstaller = "$env:TEMP\rustup-init.exe"
    
    try {
        Invoke-WebRequest -Uri $rustUrl -OutFile $rustInstaller -UseBasicParsing
        Write-Host "Installing Rust..." -ForegroundColor Yellow
        Start-Process $rustInstaller -Wait -ArgumentList "-y --default-toolchain stable"
        Remove-Item $rustInstaller -Force
        Write-Host "Rust installation completed!" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "Failed to install Rust: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

Write-Host "`nChecking current installation status..." -ForegroundColor Green

# Check current status
$nodeInstalled = Test-Command "node"
$rustInstalled = Test-Command "rustc"
$cppInstalled = Test-Command "g++"

Write-Host "Node.js: $(if($nodeInstalled){'✅ Installed'}else{'❌ Not Installed'})" -ForegroundColor $(if($nodeInstalled){'Green'}else{'Red'})
Write-Host "Rust: $(if($rustInstalled){'✅ Installed'}else{'❌ Not Installed'})" -ForegroundColor $(if($rustInstalled){'Green'}else{'Red'})
Write-Host "C++: $(if($cppInstalled){'✅ Installed'}else{'❌ Not Installed'})" -ForegroundColor $(if($cppInstalled){'Green'}else{'Red'})

if ($nodeInstalled -and $rustInstalled -and $cppInstalled) {
    Write-Host "`n🎉 All dependencies are already installed!" -ForegroundColor Green
    Write-Host "You can now run: python main.py start" -ForegroundColor Cyan
    exit 0
}

Write-Host "`n🔧 Starting installation process..." -ForegroundColor Yellow

# Install Node.js if not present
if (-not $nodeInstalled) {
    if (Install-NodeJS) {
        $env:PATH += ";$env:ProgramFiles\nodejs"
        [Environment]::SetEnvironmentVariable("PATH", $env:PATH, [EnvironmentVariableTarget]::User)
    }
}

# Install Rust if not present
if (-not $rustInstalled) {
    if (Install-Rust) {
        $env:PATH += ";$env:USERPROFILE\.cargo\bin"
        [Environment]::SetEnvironmentVariable("PATH", $env:PATH, [EnvironmentVariableTarget]::User)
    }
}

# For C++, provide manual instructions
if (-not $cppInstalled) {
    Write-Host "`n⚠️  C++ Compiler Installation Required" -ForegroundColor Yellow
    Write-Host "Please install MinGW-w64 manually:" -ForegroundColor White
    Write-Host "1. Download MSYS2 from: https://www.msys2.org/" -ForegroundColor Cyan
    Write-Host "2. Install MSYS2 and run these commands in MSYS2 terminal:" -ForegroundColor White
    Write-Host "   pacman -Syu" -ForegroundColor Gray
    Write-Host "   pacman -S mingw-w64-x86_64-gcc" -ForegroundColor Gray
    Write-Host "3. Add C:\msys64\mingw64\bin to your PATH" -ForegroundColor White
}

Write-Host "`n🎯 Installation Summary:" -ForegroundColor Green
Write-Host "✅ Node.js: $(if(-not $nodeInstalled){'Installed'}else{'Already present'})" -ForegroundColor Green
Write-Host "✅ Rust: $(if(-not $rustInstalled){'Installed'}else{'Already present'})" -ForegroundColor Green
Write-Host "⚠️  C++: Manual installation required" -ForegroundColor Yellow

Write-Host "`n🔄 Please restart your terminal and run:" -ForegroundColor Cyan
Write-Host "python main.py start" -ForegroundColor White

Write-Host "`n📋 To verify installation, run:" -ForegroundColor Yellow
Write-Host "node --version" -ForegroundColor Gray
Write-Host "rustc --version" -ForegroundColor Gray
Write-Host "g++ --version" -ForegroundColor Gray
