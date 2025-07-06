# PowerShell Script to Fix PATH Environment Variables
Write-Host "Fixing PATH Environment Variables..." -ForegroundColor Cyan

# Function to add to PATH if not already present
function Add-ToPath {
    param(
        [string]$NewPath,
        [string]$Description
    )

    if (Test-Path $NewPath) {
        $currentPath = [Environment]::GetEnvironmentVariable("PATH", [EnvironmentVariableTarget]::User)

        if ($currentPath -notlike "*$NewPath*") {
            Write-Host "Adding $Description to PATH..." -ForegroundColor Yellow
            $newPathValue = $currentPath + ";" + $NewPath
            [Environment]::SetEnvironmentVariable("PATH", $newPathValue, [EnvironmentVariableTarget]::User)
            Write-Host "Added: $NewPath" -ForegroundColor Green
        } else {
            Write-Host "Already in PATH: $Description" -ForegroundColor Blue
        }
    } else {
        Write-Host "Path not found: $NewPath" -ForegroundColor Red
    }
}

# Check and add Node.js
Write-Host "Node.js Configuration:" -ForegroundColor Yellow
$nodePaths = @(
    "C:\Program Files\nodejs",
    "C:\Program Files (x86)\nodejs"
)

foreach ($path in $nodePaths) {
    Add-ToPath -NewPath $path -Description "Node.js"
}

# Check and add Rust
Write-Host "Rust Configuration:" -ForegroundColor Yellow
$rustPath = "$env:USERPROFILE\.cargo\bin"
Add-ToPath -NewPath $rustPath -Description "Rust Cargo"

# Check and add C++ (MinGW if available)
Write-Host "C++ Configuration:" -ForegroundColor Yellow
$cppPaths = @(
    "C:\msys64\mingw64\bin",
    "C:\MinGW\bin",
    "C:\Program Files\Git\mingw64\bin"
)

foreach ($path in $cppPaths) {
    Add-ToPath -NewPath $path -Description "C++ Compiler"
}

# Refresh environment variables for current session
Write-Host "Refreshing Environment Variables..." -ForegroundColor Cyan
$env:PATH = [System.Environment]::GetEnvironmentVariable("PATH","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH","User")

Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "1. Close this terminal completely" -ForegroundColor White
Write-Host "2. Open a new terminal/PowerShell" -ForegroundColor White
Write-Host "3. Run: python check_installations.py" -ForegroundColor White
Write-Host "4. Run: python main.py start" -ForegroundColor White

Write-Host "PATH has been updated! Restart terminal to apply changes." -ForegroundColor Green
