# Local Backend Setup Guide

This guide helps you run the Swap backend services locally without Docker.

## Prerequisites

- Python 3.12+ (you have 3.13.7 ✓)
- PostgreSQL 15+
- Redis 7+
- Kafka (optional for async features)
- Git

## Quick Start

### 1. Install PostgreSQL & Redis

**Windows:**
```powershell
# Using Chocolatey (if installed)
choco install postgresql redis

# Or download installers from:
# PostgreSQL: https://www.postgresql.org/download/windows/
# Redis: https://github.com/microsoftarchive/redis/releases
```

### 2. Setup Virtual Environment

```powershell
cd C:\Users\Trendig Biz&Tech\Desktop\projects\swap
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Create Databases

```powershell
# Login to PostgreSQL
psql -U postgres -h localhost

# Run these commands in psql:
CREATE DATABASE auth;
CREATE DATABASE users;
CREATE DATABASE listings;
CREATE DATABASE offers;
CREATE DATABASE payments;
CREATE DATABASE notifications;
CREATE DATABASE chat;
CREATE DATABASE admin;

# Exit psql
\q
```

### 5. Environment Setup

Create `.env` file in root:

```env
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/auth
REDIS_URL=redis://localhost:6379/0
KAFKA_BOOTSTRAP_SERVERS=localhost:9092

# JWT
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Services
ADMIN_DATABASE_URL=postgresql://postgres:password@localhost:5432/admin
OFFER_DATABASE_URL=postgresql://postgres:password@localhost:5432/offers
PAYMENT_DATABASE_URL=postgresql://postgres:password@localhost:5432/payments

# MinIO (optional, for file uploads)
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
```

### 6. Start Services Locally

**Terminal 1 - Auth Service (Port 8000):**
```powershell
cd services\auth
set PYTHONPATH=.;..\..\shared
uvicorn main:app --reload --port 8000
```

**Terminal 2 - User Service (Port 8001):**
```powershell
cd services\user
set PYTHONPATH=.;..\..\shared
uvicorn main:app --reload --port 8001
```

**Terminal 3 - Listing Service (Port 8002):**
```powershell
cd services\listing
set PYTHONPATH=.;..\..\shared
uvicorn main:app --reload --port 8002
```

**Terminal 4 - Offer Service (Port 8003):**
```powershell
cd services\offer
set PYTHONPATH=.;..\..\shared
uvicorn main:app --reload --port 8003
```

**Terminal 5 - Payment Service (Port 8004):**
```powershell
cd services\payment
set PYTHONPATH=.;..\..\shared
uvicorn main:app --reload --port 8004
```

**Terminal 6 - Chat Service (Port 8006):**
```powershell
cd services\chat
set PYTHONPATH=.;..\..\shared
uvicorn main:app --reload --port 8006
```

**Terminal 7 - Notification Service (Port 8007):**
```powershell
cd services\notification
set PYTHONPATH=.;..\..\shared
uvicorn main:app --reload --port 8007
```

**Terminal 8 - Admin Service (Port 8005):**
```powershell
cd services\admin
python manage.py migrate
python manage.py runserver 0.0.0.0:8005
```

## Service Endpoints

| Service | Port | URL | Docs |
|---------|------|-----|------|
| Auth | 8000 | http://localhost:8000 | http://localhost:8000/docs |
| User | 8001 | http://localhost:8001 | http://localhost:8001/docs |
| Listing | 8002 | http://localhost:8002 | http://localhost:8002/docs |
| Offer | 8003 | http://localhost:8003 | http://localhost:8003/docs |
| Payment | 8004 | http://localhost:8004 | http://localhost:8004/docs |
| Chat | 8006 | http://localhost:8006 | http://localhost:8006/docs |
| Notification | 8007 | http://localhost:8007 | http://localhost:8007/docs |
| Admin (Django) | 8005 | http://localhost:8005 | http://localhost:8005/admin |
| Nginx (Gateway) | 8080 | http://localhost:8080 | - |

## Testing the Backend

```powershell
# Test Auth Service
curl http://localhost:8000/health

# Test User Service
curl http://localhost:8001/health

# Access all services through Nginx
curl http://localhost:8080/health
```

## Running All Services at Once

Use the startup script (if created):
```powershell
.\run_services_local.ps1
```

## Troubleshooting

### PostgreSQL Connection Error
- Verify PostgreSQL is running: `pg_isready -h localhost`
- Check credentials in `.env` file
- Ensure all databases are created

### Redis Connection Error
- Verify Redis is running
- Default: `redis-cli ping` should return `PONG`

### Kafka Connection Error
- For development, you can mock Kafka
- Update `KAFKA_BOOTSTRAP_SERVERS` in `.env` to skip Kafka if not needed

### Module Import Errors
- Ensure `PYTHONPATH` includes shared folder
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

## Notes

- Services use `--reload` flag for hot reloading during development
- Each service has its own database for separation of concerns
- Async features (Kafka, Redis) are optional for basic testing
- Admin service uses Django (separate from FastAPI services)

