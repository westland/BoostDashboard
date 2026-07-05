# PowerShell Installer for Windows 11 - WoW Boost Lead System
$ErrorActionPreference = "Stop"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "🚀 WoW Boost Lead System Installer for Windows 11" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Verify Python Installation
Write-Host "🔍 Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✅ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not installed or not added to your PATH environment variable." -ForegroundColor Red
    Write-Host "Please install Python 3.10+ and select 'Add python.exe to PATH' during installation." -ForegroundColor Yellow
    exit 1
}

# 2. Setup Virtual Environment
if (-not (Test-Path ".venv")) {
    Write-Host "📦 Creating virtual environment in .venv directory..." -ForegroundColor Yellow
    python -m venv .venv
    Write-Host "✅ Virtual environment created." -ForegroundColor Green
} else {
    Write-Host "✅ Virtual environment folder (.venv) already exists." -ForegroundColor Green
}

# 3. Upgrade pip and Install dependencies
Write-Host "⚡ Installing project dependencies (this may take a couple of minutes)..." -ForegroundColor Yellow
& .venv\Scripts\python.exe -m pip install --upgrade pip

# Install dependencies explicitly to prevent editable install issues during global package search
& .venv\Scripts\pip.exe install crewai crewai-tools praw discord.py streamlit pandas schedule python-dotenv langchain-google-genai nest-asyncio pyyaml

Write-Host "✅ Dependencies installed." -ForegroundColor Green

# 4. Handle .env configuration file
if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Write-Host "📝 Creating .env file from template .env.example..." -ForegroundColor Yellow
        Copy-Item .env.example .env
        Write-Host "⚠️ Please remember to review the .env file and fill in your Reddit/Discord API credentials." -ForegroundColor DarkYellow
    } else {
        Write-Host "❌ .env.example template file is missing. Could not create default .env." -ForegroundColor Red
    }
} else {
    Write-Host "✅ .env configuration file already exists." -ForegroundColor Green
}

# 5. Create quick-start launch shortcuts
Write-Host "💾 Generating Windows batch shortcuts..." -ForegroundColor Yellow

# Dashboard startup shortcut
$dashboardBat = "@echo off`r`ncd /d %~dp0`r`ncall .venv\Scripts\activate.bat`r`nstreamlit run dashboard.py`r`npause"
$dashboardBat | Out-File -FilePath "start_dashboard.bat" -Encoding ascii -NoNewline

# Scraper startup shortcut
$scraperBat = "@echo off`r`ncd /d %~dp0`r`ncall .venv\Scripts\activate.bat`r`npython -m src.wow_boosting_leads.main`r`npause"
$scraperBat | Out-File -FilePath "run_scraper.bat" -Encoding ascii -NoNewline

# Scheduler startup shortcut
$schedulerBat = "@echo off`r`ncd /d %~dp0`r`ncall .venv\Scripts\activate.bat`r`npython scheduler.py`r`npause"
$schedulerBat | Out-File -FilePath "start_scheduler.bat" -Encoding ascii -NoNewline

Write-Host "✅ Created: start_dashboard.bat" -ForegroundColor Green
Write-Host "✅ Created: run_scraper.bat" -ForegroundColor Green
Write-Host "✅ Created: start_scheduler.bat" -ForegroundColor Green

# 6. Create Desktop Shortcut
Write-Host "🖥️ Creating Desktop shortcut..." -ForegroundColor Yellow
try {
    $WshShell = New-Object -ComObject WScript.Shell
    $DesktopPath = [System.Environment]::GetFolderPath('Desktop')
    $Shortcut = $WshShell.CreateShortcut("$DesktopPath\WoW PvP Lead Control Center.lnk")
    
    $ScriptDir = if ($PSScriptRoot) { $PSScriptRoot } else { $PWD.ProviderPath }
    $Shortcut.TargetPath = "$ScriptDir\start_dashboard.bat"
    $Shortcut.WorkingDirectory = "$ScriptDir"
    $Shortcut.Description = "WoW PvP Lead Control Center Dashboard"
    $Shortcut.IconLocation = "%SystemRoot%\System32\imageres.dll, 262"
    $Shortcut.Save()
    Write-Host "✅ Created Desktop shortcut: WoW PvP Lead Control Center.lnk" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Failed to create Desktop shortcut: $_" -ForegroundColor Yellow
}

Write-Host "----------------------------------------------------------" -ForegroundColor Cyan
Write-Host "🎉 Installation Completed Successfully!" -ForegroundColor Green
Write-Host "You can now run 'start_dashboard.bat' or use the Desktop shortcut to view the UI." -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
