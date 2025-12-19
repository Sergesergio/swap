#!/usr/bin/env pwsh
# Local Development Server Startup Script
# Run all Swap backend services locally

param(
    [switch]$verbose = $false,
    [switch]$skipAdmin = $false,
    [switch]$skipKafka = $false
)

$ErrorActionPreference = "Stop"
$VerbosePreference = if ($verbose) { "Continue" } else { "SilentlyContinue" }

Write-Host "════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  Swap Platform - Local Backend Services Starter" -ForegroundColor Green
Write-Host "════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Check if venv is activated
if (-not (Test-Path ".\venv\Scripts\Activate.ps1")) {
    Write-Host "❌ Virtual environment not found. Creating one..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate venv
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Blue
& ".\venv\Scripts\Activate.ps1"

# Check Python
$pythonVersion = python --version 2>&1
Write-Host "✓ Using: $pythonVersion" -ForegroundColor Green

# Check PostgreSQL
Write-Host ""
Write-Host "🔍 Checking PostgreSQL..." -ForegroundColor Blue
try {
    $pgReady = pg_isready -h localhost 2>&1
    Write-Host "✓ PostgreSQL is running" -ForegroundColor Green
}
catch {
    Write-Host "⚠ PostgreSQL not accessible. Please ensure it's running:" -ForegroundColor Yellow
    Write-Host "  Windows: Start PostgreSQL from Services or use 'pg_ctl start'" -ForegroundColor Gray
    Write-Host "  psql -U postgres" -ForegroundColor Gray
}

# Check Redis
Write-Host "🔍 Checking Redis..." -ForegroundColor Blue
try {
    $redisReady = redis-cli ping 2>&1
    if ($redisReady -eq "PONG") {
        Write-Host "✓ Redis is running" -ForegroundColor Green
    }
}
catch {
    Write-Host "⚠ Redis not accessible. Please ensure it's running:" -ForegroundColor Yellow
    Write-Host "  Windows: Start Redis from Services or redis-server" -ForegroundColor Gray
}

Write-Host ""
Write-Host "════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "Starting Services..." -ForegroundColor Green
Write-Host "════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Define services
$services = @(
    @{name = "Auth"; port = 8000; path = "services\auth"; cmd = "uvicorn main:app --reload --host 0.0.0.0 --port 8000"},
    @{name = "User"; port = 8001; path = "services\user"; cmd = "uvicorn main:app --reload --host 0.0.0.0 --port 8001"},
    @{name = "Listing"; port = 8002; path = "services\listing"; cmd = "uvicorn main:app --reload --host 0.0.0.0 --port 8002"},
    @{name = "Offer"; port = 8003; path = "services\offer"; cmd = "uvicorn main:app --reload --host 0.0.0.0 --port 8003"},
    @{name = "Payment"; port = 8004; path = "services\payment"; cmd = "uvicorn main:app --reload --host 0.0.0.0 --port 8004"},
    @{name = "Chat"; port = 8006; path = "services\chat"; cmd = "uvicorn main:app --reload --host 0.0.0.0 --port 8006"},
    @{name = "Notification"; port = 8007; path = "services\notification"; cmd = "uvicorn main:app --reload --host 0.0.0.0 --port 8007"}
)

# Add Admin if not skipped
if (-not $skipAdmin) {
    $services += @{name = "Admin (Django)"; port = 8005; path = "services\admin"; cmd = "python manage.py runserver 0.0.0.0:8005"}
}

Write-Host "📋 Services to start:" -ForegroundColor Cyan
foreach ($service in $services) {
    Write-Host "   • $($service.name) on port $($service.port)" -ForegroundColor White
}
Write-Host ""

Write-Host "⏳ Starting services in separate windows..." -ForegroundColor Green
Write-Host "   (Each service will open in its own PowerShell window)" -ForegroundColor Gray
Write-Host ""

# Start each service in a new window
foreach ($service in $services) {
    $title = "$($service.name) Service (Port $($service.port))"
    
    $cmd = @"
`$env:PYTHONPATH = ".;..\..\shared"
cd "$((Get-Location).Path)\$($service.path)"
Write-Host "Starting $($service.name) Service..."
$($service.cmd)
"@
    
    Write-Host "→ Opening $title" -ForegroundColor Blue
    Start-Process pwsh -ArgumentList "-NoExit", "-Command", $cmd -WindowStyle Normal
    Start-Sleep -Milliseconds 500
}

Write-Host ""
Write-Host "════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "✅ All services started!" -ForegroundColor Green
Write-Host "════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "🌐 Access your services at:" -ForegroundColor Green
Write-Host ""
Write-Host "  Auth Service:         http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "  User Service:         http://localhost:8001/docs" -ForegroundColor Cyan
Write-Host "  Listing Service:      http://localhost:8002/docs" -ForegroundColor Cyan
Write-Host "  Offer Service:        http://localhost:8003/docs" -ForegroundColor Cyan
Write-Host "  Payment Service:      http://localhost:8004/docs" -ForegroundColor Cyan
Write-Host "  Chat Service:         http://localhost:8006/docs" -ForegroundColor Cyan
Write-Host "  Notification Service: http://localhost:8007/docs" -ForegroundColor Cyan
if (-not $skipAdmin) {
    Write-Host "  Admin (Django):       http://localhost:8005/admin" -ForegroundColor Cyan
}
Write-Host ""
Write-Host "  API Gateway (Nginx):  http://localhost:8080/health" -ForegroundColor Yellow
Write-Host ""
Write-Host "📖 Local Setup Guide: see LOCAL_SETUP.md" -ForegroundColor Green
Write-Host ""
