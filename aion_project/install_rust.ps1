# PowerShell Script to Install Rust
Write-Host "Installing Rust Programming Language..." -ForegroundColor Cyan

# Check if Rust is already installed
$rustPath = "$env:USERPROFILE\.cargo\bin\rustc.exe"
if (Test-Path $rustPath) {
    Write-Host "Rust is already installed!" -ForegroundColor Green
    & $rustPath --version
    exit 0
}

# Download Rust installer
$rustInstaller = "$env:TEMP\rustup-init.exe"
$rustUrl = "https://static.rust-lang.org/rustup/dist/x86_64-pc-windows-msvc/rustup-init.exe"

Write-Host "Downloading Rust installer..." -ForegroundColor Yellow
try {
    Invoke-WebRequest -Uri $rustUrl -OutFile $rustInstaller -UseBasicParsing
    Write-Host "Download completed!" -ForegroundColor Green
} catch {
    Write-Host "Failed to download Rust installer: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Please download manually from: https://rustup.rs/" -ForegroundColor Yellow
    exit 1
}

# Install Rust
Write-Host "Installing Rust..." -ForegroundColor Yellow
try {
    Start-Process $rustInstaller -Wait -ArgumentList "-y --default-toolchain stable"
    Write-Host "Rust installation completed!" -ForegroundColor Green
    
    # Clean up
    Remove-Item $rustInstaller -Force
    
    # Add to PATH
    $cargoPath = "$env:USERPROFILE\.cargo\bin"
    $currentPath = [Environment]::GetEnvironmentVariable("PATH", [EnvironmentVariableTarget]::User)
    
    if ($currentPath -notlike "*$cargoPath*") {
        Write-Host "Adding Rust to PATH..." -ForegroundColor Yellow
        $newPathValue = $currentPath + ";" + $cargoPath
        [Environment]::SetEnvironmentVariable("PATH", $newPathValue, [EnvironmentVariableTarget]::User)
        Write-Host "Rust added to PATH!" -ForegroundColor Green
    }
    
    # Refresh PATH for current session
    $env:PATH += ";$cargoPath"
    
    # Test installation
    Write-Host "Testing Rust installation..." -ForegroundColor Cyan
    if (Test-Path "$cargoPath\rustc.exe") {
        $version = & "$cargoPath\rustc.exe" --version
        Write-Host "Success! Rust version: $version" -ForegroundColor Green
    } else {
        Write-Host "Installation completed but rustc not found. Please restart terminal." -ForegroundColor Yellow
    }
    
} catch {
    Write-Host "Failed to install Rust: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Please install manually from: https://rustup.rs/" -ForegroundColor Yellow
    exit 1
}

Write-Host "Rust installation completed successfully!" -ForegroundColor Green
Write-Host "Please restart your terminal to use Rust commands." -ForegroundColor Cyan
