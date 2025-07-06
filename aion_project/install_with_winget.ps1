# AION Requirements Installation using Winget
# تثبيت متطلبات AION باستخدام Winget

Write-Host "🚀 AION Requirements Installation with Winget" -ForegroundColor Cyan
Write-Host "تثبيت متطلبات AION باستخدام Winget" -ForegroundColor Cyan
Write-Host "=" * 50

# Function to check if a command exists
function Test-Command($cmdname) {
    return [bool](Get-Command -Name $cmdname -ErrorAction SilentlyContinue)
}

# Check if Winget is available
if (-not (Test-Command winget)) {
    Write-Host "❌ Winget is not available on this system" -ForegroundColor Red
    Write-Host "❌ Winget غير متوفر على هذا النظام" -ForegroundColor Red
    Write-Host "Please use the install_requirements.ps1 script instead" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✅ Winget is available" -ForegroundColor Green

# Install Node.js
Write-Host "`n🟨 Installing Node.js..." -ForegroundColor Yellow
if (-not (Test-Command node)) {
    winget install OpenJS.NodeJS
    Write-Host "✅ Node.js installation completed" -ForegroundColor Green
} else {
    Write-Host "✅ Node.js already installed" -ForegroundColor Green
    node --version
}

# Install Rust
Write-Host "`n🦀 Installing Rust..." -ForegroundColor Yellow
if (-not (Test-Command rustc)) {
    winget install Rustlang.Rustup
    Write-Host "✅ Rust installation completed" -ForegroundColor Green
} else {
    Write-Host "✅ Rust already installed" -ForegroundColor Green
    rustc --version
}

# Install MinGW-w64
Write-Host "`n⚡ Installing MinGW-w64..." -ForegroundColor Yellow
if (-not (Test-Command g++)) {
    winget install mingw-w64
    Write-Host "✅ MinGW-w64 installation completed" -ForegroundColor Green
} else {
    Write-Host "✅ MinGW-w64 already installed" -ForegroundColor Green
    g++ --version
}

Write-Host "`n🔄 Please restart your terminal to refresh PATH variables" -ForegroundColor Yellow
Write-Host "🔄 يرجى إعادة تشغيل الطرفية لتحديث متغيرات PATH" -ForegroundColor Yellow

Write-Host "`n🎉 Installation completed!" -ForegroundColor Green
Write-Host "🎉 تم الانتهاء من التثبيت!" -ForegroundColor Green

Read-Host "`nPress Enter to exit | اضغط Enter للخروج"
