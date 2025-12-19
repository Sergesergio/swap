#!/usr/bin/env pwsh
# PostgreSQL Setup Script for Local Development
# Creates all necessary databases for Swap services

param(
    [string]$host = "localhost",
    [string]$user = "postgres",
    [string]$port = 5432,
    [switch]$verbose = $false
)

$VerbosePreference = if ($verbose) { "Continue" } else { "SilentlyContinue" }

Write-Host "════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  Swap Platform - PostgreSQL Database Setup" -ForegroundColor Green
Write-Host "════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Check if PostgreSQL is running
Write-Host "🔍 Checking PostgreSQL connection..." -ForegroundColor Blue
try {
    $pgReady = pg_isready -h $host -p $port -U $user 2>&1
    if ($pgReady -match "accepting connections") {
        Write-Host "✓ PostgreSQL is running and accepting connections" -ForegroundColor Green
    } else {
        Write-Host "✗ PostgreSQL is not accepting connections" -ForegroundColor Red
        Write-Host "  Please start PostgreSQL service and try again" -ForegroundColor Gray
        exit 1
    }
}
catch {
    Write-Host "✗ Cannot connect to PostgreSQL" -ForegroundColor Red
    Write-Host "  Error: $_" -ForegroundColor Gray
    exit 1
}

Write-Host ""
Write-Host "📝 Databases to create:" -ForegroundColor Cyan
$databases = @("auth", "users", "listings", "offers", "payments", "notifications", "chat", "admin")
$databases | ForEach-Object { Write-Host "   • $_" -ForegroundColor White }
Write-Host ""

# Create SQL script
$sqlScript = @"
-- Create databases for each service
CREATE DATABASE IF NOT EXISTS auth;
CREATE DATABASE IF NOT EXISTS users;
CREATE DATABASE IF NOT EXISTS listings;
CREATE DATABASE IF NOT EXISTS offers;
CREATE DATABASE IF NOT EXISTS payments;
CREATE DATABASE IF NOT EXISTS notifications;
CREATE DATABASE IF NOT EXISTS chat;
CREATE DATABASE IF NOT EXISTS admin;

-- Display results
\l
"@ -replace "IF NOT EXISTS", ""  # Remove for PostgreSQL compatibility

Write-Host "🔧 Creating databases..." -ForegroundColor Blue

foreach ($db in $databases) {
    try {
        # Use psql to create database
        $createCmd = "CREATE DATABASE `"$db`";"
        $psqlCmd = $createCmd | & psql -h $host -U $user -p $port 2>&1
        
        if ($psqlCmd -match "already exists" -or $psqlCmd -match "CREATE DATABASE") {
            Write-Host "✓ Database '$db' ready" -ForegroundColor Green
        }
    }
    catch {
        Write-Host "✗ Failed to create database '$db'" -ForegroundColor Red
        Write-Host "  Error: $_" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "✓ Verifying databases..." -ForegroundColor Blue

# List all databases
$listCmd = "SELECT datname FROM pg_database WHERE datname IN ('auth', 'users', 'listings', 'offers', 'payments', 'notifications', 'chat', 'admin') ORDER BY datname;"
$result = $listCmd | & psql -h $host -U $user -p $port -t 2>&1

$createdDbs = @()
foreach ($line in $result) {
    $trimmed = $line.Trim()
    if ($trimmed -and $trimmed -ne "datname" -and $trimmed -ne "-") {
        $createdDbs += $trimmed
    }
}

Write-Host ""
Write-Host "📊 Database Status:" -ForegroundColor Cyan
foreach ($db in $databases) {
    if ($createdDbs -contains $db) {
        Write-Host "✓ $db" -ForegroundColor Green
    } else {
        Write-Host "✗ $db" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "════════════════════════════════════════════════════" -ForegroundColor Cyan
if ($createdDbs.Count -eq $databases.Count) {
    Write-Host "✅ All databases created successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Green
    Write-Host "  1. Create .env file with connection strings" -ForegroundColor Gray
    Write-Host "  2. Update requirements.txt if needed" -ForegroundColor Gray
    Write-Host "  3. Run: .\run_services_local.ps1" -ForegroundColor Gray
} else {
    Write-Host "⚠ Some databases were not created successfully" -ForegroundColor Yellow
}
Write-Host "════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Display connection strings
Write-Host "🔗 Connection Strings for .env:" -ForegroundColor Green
Write-Host ""
Write-Host "# PostgreSQL (use one of these for each service)" -ForegroundColor Gray
$databases | ForEach-Object {
    Write-Host "postgresql://postgres:password@$($host):$($port)/$_" -ForegroundColor Yellow
}
Write-Host ""
