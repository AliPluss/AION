# Fix Python PATH issue in Windows
# Run this script as Administrator

Write-Host "🔧 Fixing Python PATH issue..." -ForegroundColor Green

# Get current user's Python Scripts path
$pythonScriptsPath = "$env:LOCALAPPDATA\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\Scripts"

Write-Host "📍 Python Scripts Path: $pythonScriptsPath" -ForegroundColor Yellow

# Check if path exists
if (Test-Path $pythonScriptsPath) {
    Write-Host "✅ Python Scripts directory found" -ForegroundColor Green
    
    # Get current PATH
    $currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
    
    # Check if already in PATH
    if ($currentPath -like "*$pythonScriptsPath*") {
        Write-Host "✅ Path already exists in PATH" -ForegroundColor Green
    } else {
        Write-Host "➕ Adding to PATH..." -ForegroundColor Yellow
        
        # Add to user PATH
        $newPath = $currentPath + ";" + $pythonScriptsPath
        [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
        
        Write-Host "✅ Path added to USER PATH successfully!" -ForegroundColor Green
        Write-Host "🔄 Please restart your terminal/IDE to apply changes" -ForegroundColor Cyan
    }
} else {
    Write-Host "❌ Python Scripts directory not found" -ForegroundColor Red
    Write-Host "📍 Expected path: $pythonScriptsPath" -ForegroundColor Yellow
}

# Alternative: Show how to use python -m
Write-Host "`n💡 Alternative Solutions:" -ForegroundColor Cyan
Write-Host "1. Use 'python -m flake8' instead of 'flake8'" -ForegroundColor White
Write-Host "2. Use 'python -m pytest' instead of 'pytest'" -ForegroundColor White
Write-Host "3. Use 'python -m black' instead of 'black'" -ForegroundColor White

# Test current setup
Write-Host "`n🧪 Testing current setup:" -ForegroundColor Cyan
try {
    $pythonVersion = python --version
    Write-Host "✅ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found in PATH" -ForegroundColor Red
}

try {
    $pipVersion = python -m pip --version
    Write-Host "✅ Pip: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Pip not accessible" -ForegroundColor Red
}

Write-Host "`n🎉 PATH fix script completed!" -ForegroundColor Green
