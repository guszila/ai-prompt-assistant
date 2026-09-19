# Start Desktop Application in development mode
Write-Host "Starting Desktop Development..." -ForegroundColor Cyan

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptPath
$desktopPath = Join-Path $projectRoot "apps\desktop"

Set-Location $desktopPath

npm run dev
