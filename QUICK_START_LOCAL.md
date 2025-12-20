# 🚀 Quick Start - Run Backend Locally (No Docker)

## Prerequisites (5 minutes)

1. **Python 3.10+** - [Download](https://www.python.org/downloads/)
2. **PostgreSQL 15+** - [Download](https://www.postgresql.org/download/)
3. **Redis 7+** - [Download](https://github.com/microsoftarchive/redis/releases)
4. **Git** - (already installed if you cloned this)

## Setup Steps

### 1️⃣ Create PostgreSQL Databases

```powershell
psql -U postgres

-- Then run these 8 commands:
CREATE DATABASE auth;
CREATE DATABASE users;
CREATE DATABASE listings;
CREATE DATABASE offers;
CREATE DATABASE payments;
CREATE DATABASE notifications;
CREATE DATABASE chat;
CREATE DATABASE admin;

\q
```

### 2️⃣ Create Python Virtual Environment

```powershell
cd C:\Users\Trendig Biz&Tech\Desktop\projects\swap
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3️⃣ Configure Environment

Copy `.env.example` to `.env`:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and update these if your PostgreSQL password is different:

```env
DATABASE_URL=postgresql://postgres:PASSWORD@localhost:5432/auth
USER_DATABASE_URL=postgresql://postgres:PASSWORD@localhost:5432/users
# ... etc for all databases
```

### 4️⃣ Start Services

**Start each in a NEW terminal window:**

```powershell
# Terminal 1 - Auth (Port 8000)
cd services\auth
set PYTHONPATH=.;..\..\shared
uvicorn main:app --reload --port 8000
```

```powershell
# Terminal 2 - User (Port 8001)
cd services\user
set PYTHONPATH=.;..\..\shared
uvicorn main:app --reload --port 8001
```

```powershell
# Terminal 3 - Listing (Port 8002)
cd services\listing
set PYTHONPATH=.;..\..\shared
uvicorn main:app --reload --port 8002
```

```powershell
# Terminal 4 - Offer (Port 8003)
cd services\offer
set PYTHONPATH=.;..\..\shared
uvicorn main:app --reload --port 8003
```

```powershell
# Terminal 5 - Payment (Port 8004)
cd services\payment
set PYTHONPATH=.;..\..\shared
uvicorn main:app --reload --port 8004
```

```powershell
# Terminal 6 - Chat (Port 8006)
cd services\chat
set PYTHONPATH=.;..\..\shared
uvicorn main:app --reload --port 8006
```

```powershell
# Terminal 7 - Notification (Port 8007)
cd services\notification
set PYTHONPATH=.;..\..\shared
uvicorn main:app --reload --port 8007
```

```powershell
# Terminal 8 - Admin (Port 8005)
cd services\admin
python manage.py migrate
python manage.py runserver 0.0.0.0:8005
```

## ✅ Verify Services

Open in your browser:

- Auth: http://localhost:8000/docs
- User: http://localhost:8001/docs
- Listing: http://localhost:8002/docs
- Offer: http://localhost:8003/docs
- Payment: http://localhost:8004/docs
- Chat: http://localhost:8006/docs
- Notification: http://localhost:8007/docs
- Admin: http://localhost:8005/admin

Or test via command:

```powershell
curl http://localhost:8000/health
```

## 🛠️ Troubleshooting

### Import Errors

```powershell
# Ensure PYTHONPATH includes shared:
$env:PYTHONPATH = ".;../../shared"
```

### PostgreSQL Connection Error

```powershell
# Check if PostgreSQL is running:
psql -U postgres -c "SELECT 1"

# Check databases exist:
psql -U postgres -l
```

### Dependencies Missing

```powershell
pip install -r requirements.txt --force-reinstall
```

## 📚 Full Guide

See `LOCAL_SETUP.md` for detailed instructions including:

- Kafka setup (optional)
- MinIO configuration
- Email/SMTP setup
- Docker Compose for external services

---

**Done!** Your backend is now running locally. Start developing! 🎉
