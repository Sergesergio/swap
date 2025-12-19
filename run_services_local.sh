#!/bin/bash
# Local Development Server Startup Script (Linux/Mac)
# Run all Swap backend services locally

set -e

VERBOSE=false
SKIP_ADMIN=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -v|--verbose) VERBOSE=true; shift ;;
        --skip-admin) SKIP_ADMIN=true; shift ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

echo "════════════════════════════════════════════════════"
echo "  Swap Platform - Local Backend Services Starter"
echo "════════════════════════════════════════════════════"
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check Python
PYTHON_VERSION=$(python --version)
echo "✓ Using: $PYTHON_VERSION"

# Check PostgreSQL
echo ""
echo "🔍 Checking PostgreSQL..."
if pg_isready -h localhost > /dev/null 2>&1; then
    echo "✓ PostgreSQL is running"
else
    echo "⚠ PostgreSQL not accessible. Please ensure it's running."
    echo "  brew install postgresql (Mac)"
    echo "  apt-get install postgresql (Linux)"
fi

# Check Redis
echo "🔍 Checking Redis..."
if redis-cli ping > /dev/null 2>&1; then
    echo "✓ Redis is running"
else
    echo "⚠ Redis not accessible. Please ensure it's running."
    echo "  brew install redis (Mac)"
    echo "  apt-get install redis-server (Linux)"
fi

echo ""
echo "════════════════════════════════════════════════════"
echo "Starting Services..."
echo "════════════════════════════════════════════════════"
echo ""

# Define services
declare -a SERVICES=(
    "Auth|8000|services/auth|uvicorn main:app --reload --host 0.0.0.0 --port 8000"
    "User|8001|services/user|uvicorn main:app --reload --host 0.0.0.0 --port 8001"
    "Listing|8002|services/listing|uvicorn main:app --reload --host 0.0.0.0 --port 8002"
    "Offer|8003|services/offer|uvicorn main:app --reload --host 0.0.0.0 --port 8003"
    "Payment|8004|services/payment|uvicorn main:app --reload --host 0.0.0.0 --port 8004"
    "Chat|8006|services/chat|uvicorn main:app --reload --host 0.0.0.0 --port 8006"
    "Notification|8007|services/notification|uvicorn main:app --reload --host 0.0.0.0 --port 8007"
)

if [ "$SKIP_ADMIN" = false ]; then
    SERVICES+=("Admin|8005|services/admin|python manage.py runserver 0.0.0.0:8005")
fi

echo "📋 Services to start:"
for SERVICE in "${SERVICES[@]}"; do
    IFS='|' read -r name port path cmd <<< "$SERVICE"
    echo "   • $name on port $port"
done
echo ""

echo "⏳ Starting services in separate terminals..."
echo "   (Each service will open in its own terminal)" 
echo ""

# Start each service
for SERVICE in "${SERVICES[@]}"; do
    IFS='|' read -r name port path cmd <<< "$SERVICE"
    
    echo "→ Opening $name Service (Port $port)"
    
    SHELL_CMD="cd '$PWD/$path' && export PYTHONPATH='.;../../shared' && $cmd"
    
    # Use different terminal based on OS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        osascript -e "tell app \"Terminal\" to do script \"$SHELL_CMD\""
    else
        # Linux
        gnome-terminal -- bash -c "$SHELL_CMD; exec bash"
    fi
    
    sleep 0.5
done

echo ""
echo "════════════════════════════════════════════════════"
echo "✅ All services started!"
echo "════════════════════════════════════════════════════"
echo ""
echo "🌐 Access your services at:"
echo ""
echo "  Auth Service:         http://localhost:8000/docs"
echo "  User Service:         http://localhost:8001/docs"
echo "  Listing Service:      http://localhost:8002/docs"
echo "  Offer Service:        http://localhost:8003/docs"
echo "  Payment Service:      http://localhost:8004/docs"
echo "  Chat Service:         http://localhost:8006/docs"
echo "  Notification Service: http://localhost:8007/docs"
if [ "$SKIP_ADMIN" = false ]; then
    echo "  Admin (Django):       http://localhost:8005/admin"
fi
echo ""
echo "  API Gateway (Nginx):  http://localhost:8080/health"
echo ""
echo "📖 Local Setup Guide: see LOCAL_SETUP.md"
echo ""
