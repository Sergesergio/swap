#!/usr/bin/env pwsh
# Check system requirements for local backend development

param(
    [switch]$fix = $false
)

Write-Host "════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  Swap Platform - System Requirements Check" -ForegroundColor Green
Write-Host "════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

$allGood = $true

# Check Python
Write-Host "🔍 Checking Python..." -ForegroundColor Blue
try {
    $pythonVersion = python --version 2>&1
    $version = [version]($pythonVersion -replace 'Python ', '')
    if ($version.Major -ge 3 -and $version.Minor -ge 10) {
        Write-Host "✓ $pythonVersion" -ForegroundColor Green
    } else {
        Write-Host "✗ $pythonVersion (Requires 3.10+)" -ForegroundColor Red
        $allGood = $false
    }
}
catch {
    Write-Host "✗ Python not found" -ForegroundColor Red
    Write-Host "  Install from: https://www.python.org/downloads/" -ForegroundColor Gray
    $allGood = $false
}

# Check pip
Write-Host ""
Write-Host "🔍 Checking pip..." -ForegroundColor Blue
try {
    $pipVersion = pip --version 2>&1
    Write-Host "✓ $pipVersion" -ForegroundColor Green
}
catch {
    Write-Host "✗ pip not found" -ForegroundColor Red
    $allGood = $false
}

# Check PostgreSQL
Write-Host ""
Write-Host "🔍 Checking PostgreSQL..." -ForegroundColor Blue
try {
    $pgVersion = psql --version 2>&1
    Write-Host "✓ $pgVersion" -ForegroundColor Green
    
    # Check if running
    if (pg_isready -h localhost 2>&1 | Select-String "accepting connections") {
        Write-Host "✓ PostgreSQL is running" -ForegroundColor Green
    } else {
        Write-Host "⚠ PostgreSQL is installed but not running" -ForegroundColor Yellow
        if ($fix) {
            Write-Host "  Attempting to start PostgreSQL..." -ForegroundColor Yellow
            Start-Service postgresql-x64-*
        }
    }
}
catch {
    Write-Host "✗ PostgreSQL not found" -ForegroundColor Red
    Write-Host "  Install from: https://www.postgresql.org/download/windows/" -ForegroundColor Gray
    $allGood = $false
}

# Check Redis
Write-Host ""
Write-Host "🔍 Checking Redis..." -ForegroundColor Blue
try {
    $redisVersion = redis-cli --version 2>&1
    Write-Host "✓ $redisVersion" -ForegroundColor Green
    
    # Check if running
    if (redis-cli ping 2>&1 | Select-String "PONG") {
        Write-Host "✓ Redis is running" -ForegroundColor Green
    } else {
        Write-Host "⚠ Redis is installed but not running" -ForegroundColor Yellow
        if ($fix) {
            Write-Host "  Attempting to start Redis..." -ForegroundColor Yellow
            Start-Service Redis
        }
    }
}
catch {
    Write-Host "⚠ Redis not found (Optional but recommended)" -ForegroundColor Yellow
    Write-Host "  Install from: https://github.com/microsoftarchive/redis/releases" -ForegroundColor Gray
}

# Check Git
Write-Host ""
Write-Host "🔍 Checking Git..." -ForegroundColor Blue
try {
    $gitVersion = git --version 2>&1
    Write-Host "✓ $gitVersion" -ForegroundColor Green
}
catch {
    Write-Host "⚠ Git not found (Optional)" -ForegroundColor Yellow
}

# Virtual Environment
Write-Host ""
Write-Host "🔍 Checking Virtual Environment..." -ForegroundColor Blue
if (Test-Path ".\venv\Scripts\Activate.ps1") {
    Write-Host "✓ Virtual environment found" -ForegroundColor Green
    
    if ($fix) {
        Write-Host "  Activating and upgrading pip..." -ForegroundColor Yellow
        & ".\venv\Scripts\Activate.ps1"
        python -m pip install --upgrade pip
    }
} else {
    Write-Host "⚠ Virtual environment not found" -ForegroundColor Yellow
    if ($fix) {
        Write-Host "  Creating virtual environment..." -ForegroundColor Yellow
        python -m venv venv
        & ".\venv\Scripts\Activate.ps1"
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        Write-Host "✓ Virtual environment created and dependencies installed" -ForegroundColor Green
    }
}

# Check dependencies
Write-Host ""
Write-Host "🔍 Checking Python Dependencies..." -ForegroundColor Blue
try {
    & ".\venv\Scripts\Activate.ps1"
    $deps = @("fastapi", "uvicorn", "sqlmodel", "psycopg2", "redis", "aiokafka")
    $missingDeps = @()
    
    foreach ($dep in $deps) {
        python -c "import $($dep.replace('-', '_'))" 2>$null
        if ($LASTEXITCODE -ne 0) {
            $missingDeps += $dep
        }
    }
    
    if ($missingDeps.Count -eq 0) {
        Write-Host "✓ All required dependencies installed" -ForegroundColor Green
    } else {
        Write-Host "⚠ Missing dependencies: $($missingDeps -join ', ')" -ForegroundColor Yellow
        if ($fix) {
            Write-Host "  Installing missing dependencies..." -ForegroundColor Yellow
            pip install -r requirements.txt
        }
    }
}
catch {
    Write-Host "⚠ Could not check dependencies" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "════════════════════════════════════════════════════" -ForegroundColor Cyan
if ($allGood) {
    Write-Host "✅ All requirements met! Ready to start backend." -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Green
    Write-Host "  1. Configure databases: psql -U postgres" -ForegroundColor Gray
    Write-Host "  2. Create .env file with database credentials" -ForegroundColor Gray
    Write-Host "  3. Run: .\run_services_local.ps1" -ForegroundColor Gray
} else {
    Write-Host "⚠ Some requirements are missing. Please install them." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To auto-fix issues, run: .\check_requirements.ps1 -fix" -ForegroundColor Yellow
}
Write-Host "════════════════════════════════════════════════════" -ForegroundColor Cyan
