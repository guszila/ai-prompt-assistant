# Start AI Service in development mode
Write-Host "Starting AI Service on http://127.0.0.1:8000..." -ForegroundColor Cyan

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptPath
$servicePath = Join-Path $projectRoot "apps\ai-service"

Set-Location $servicePath

if (Test-Path ".venv\Scripts\Activate.ps1") {
    & ".\.venv\Scripts\Activate.ps1"
}

uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
