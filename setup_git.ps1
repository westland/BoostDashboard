# PowerShell Script to Sync Repository to GitHub
$ErrorActionPreference = "Continue"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "Git Initializer and GitHub Pusher" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Check if git is installed
try {
    $gitVersion = git --version
    Write-Host "Found: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "Git is not installed or not in PATH." -ForegroundColor Red
    Write-Host "Please install Git from https://git-scm.com/ and try again." -ForegroundColor Yellow
    exit 1
}

# 2. Git Init
if (-not (Test-Path ".git")) {
    Write-Host "Initializing local Git repository..." -ForegroundColor Yellow
    git init
    git branch -M main
    Write-Host "Local repository initialized on branch main." -ForegroundColor Green
} else {
    Write-Host "Git repository already initialized." -ForegroundColor Green
}

# 3. Add Remote Origin
$existingRemotes = git remote
$hasOrigin = $false
if ($existingRemotes) {
    foreach ($r in $existingRemotes) {
        if ($r -eq "origin") {
            $hasOrigin = $true
        }
    }
}

if ($hasOrigin) {
    Write-Host "Remote origin already exists." -ForegroundColor Green
    $originUrl = git remote get-url origin
    Write-Host "Current origin points to: $originUrl" -ForegroundColor Gray
    
    if ($originUrl -notmatch "BoostDashboard") {
        Write-Host "Updating remote origin to https://github.com/westland/BoostDashboard.git..." -ForegroundColor Yellow
        git remote set-url origin https://github.com/westland/BoostDashboard.git
    }
} else {
    Write-Host "Adding remote origin pointing to: https://github.com/westland/BoostDashboard.git" -ForegroundColor Yellow
    git remote add origin https://github.com/westland/BoostDashboard.git
    Write-Host "Remote origin added." -ForegroundColor Green
}

# 4. Stage Files
Write-Host "Staging files..." -ForegroundColor Yellow
git add .
Write-Host "Files staged." -ForegroundColor Green

# 5. Commit
Write-Host "Creating commit..." -ForegroundColor Yellow
git commit -m "Initial commit: WoW Arena Boosting and Coaching Lead System with Gemini LLM integration"
Write-Host "Changes committed." -ForegroundColor Green

# 6. Push to GitHub
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
Write-Host "Make sure you have created the empty repository BoostDashboard on GitHub before this step!" -ForegroundColor Yellow
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "Push succeeded! Project is live on GitHub." -ForegroundColor Green
} else {
    Write-Host "Git push failed. Verify repository existence or git authentication settings." -ForegroundColor Red
}
Write-Host "==========================================================" -ForegroundColor Cyan
