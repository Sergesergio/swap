#!/usr/bin/env pwsh

Write-Host "=== Testing Swap Platform APIs ===" -ForegroundColor Cyan

# Test Auth Service
Write-Host "`n>>> AUTH SERVICE (port 8000)" -ForegroundColor Yellow

Write-Host "1. Health Check"
$health = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing
Write-Host "Response: $($health.Content)"

Write-Host "`n2. Register User"
$registerBody = @{
    email = "testuser@example.com"
    username = "testuser"
    password = "SecurePass123!"
} | ConvertTo-Json

try {
    $registerResp = Invoke-WebRequest -Uri "http://localhost:8000/register" -Method POST `
        -ContentType "application/json" -Body $registerBody -UseBasicParsing -ErrorAction Stop
    $registerResp.Content | ConvertFrom-Json | Format-List
} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test Payment Service
Write-Host "`n>>> PAYMENT SERVICE (port 8004)" -ForegroundColor Yellow

Write-Host "1. Health Check"
$health = Invoke-WebRequest -Uri "http://localhost:8004/health" -UseBasicParsing
Write-Host "Response: $($health.Content)"

# Test Offer Service
Write-Host "`n>>> OFFER SERVICE (port 8003)" -ForegroundColor Yellow

Write-Host "1. Health Check"
$health = Invoke-WebRequest -Uri "http://localhost:8003/health" -UseBasicParsing
Write-Host "Response: $($health.Content)"

Write-Host "`n=== All services are responding ===" -ForegroundColor Green
