# Swap Platform - Deployment & Startup Guide

## Quick Start

### Prerequisites

- Docker Desktop (or Docker Engine + Docker Compose)
- Git
- 8GB+ RAM available
- 20GB+ disk space

### One-Command Startup

```bash
cd /path/to/swap
docker-compose up -d --build
```

Then access:

- **Frontend**: http://localhost:3000
- **API Gateway**: http://localhost:8080
- **API Docs**: http://localhost:8080/api/auth/docs

---

## Architecture Overview

### Service Layout

```
FRONTEND (Next.js 14)
  :3000

     ↓ (HTTP Requests)

NGINX API GATEWAY
  :8080 (Rate Limiting, Caching, CORS)

     ↓ (Routes Requests)

┌─────────────────────────────────────────┐
│  MICROSERVICES (FastAPI + PostgreSQL)   │
├─────────────────────────────────────────┤
│ Auth      :8000  │ User      :8001      │
│ Listing   :8002  │ Offer     :8003      │
│ Payment   :8004  │ Admin     :8005      │
│ Chat      :8006  │ Notify    :8007      │
└─────────────────────────────────────────┘

     ↓ (Event Bus & Storage)

┌─────────────────────────────────────────┐
│  INFRASTRUCTURE                          │
├─────────────────────────────────────────┤
│ PostgreSQL :5432  (8 databases)         │
│ Redis      :6379  (caching)             │
│ Kafka      :9092  (event streaming)     │
│ MinIO      :9000  (S3-compatible)       │
│ MailHog    :1025  (email testing)       │
└─────────────────────────────────────────┘
```

---

## Detailed Startup Process

### Step 1: Clean Previous Builds (Optional)

```bash
cd /path/to/swap

# Remove stopped containers
docker-compose down

# Remove volumes (resets all databases)
docker-compose down -v

# Remove dangling images
docker image prune -f
```

### Step 2: Start Services

```bash
# Build images and start all services
docker-compose up -d --build

# Watch the startup progress
docker-compose logs -f
```

### Step 3: Verify All Services Are Healthy

```bash
# Check all services
docker-compose ps

# Expected output: All services should show "Up" status

# Check specific service
docker-compose logs postgres    # or any service name
```

**Typical startup time**: 2-3 minutes (first run), 30-60 seconds (subsequent runs)

---

## Service Startup Order

Docker-compose automatically manages dependencies, but services start in this order:

1. **Infrastructure First** (2-3 min):

   - PostgreSQL (initializes 8 databases)
   - Redis
   - Zookeeper → Kafka
   - MinIO
   - MailHog

2. **Backend Services** (1-2 min):

   - Auth Service
   - User Service
   - Listing Service
   - Offer Service
   - Payment Service
   - Chat Service
   - Notification Service
   - Admin Service

3. **API Gateway** (30 sec):

   - Nginx (waits for all backends to be ready)

4. **Frontend** (1 min):
   - Next.js (builds and starts)

---

## Accessing the Application

### Frontend

```
http://localhost:3000/
```

**Pages**:

- `/auth/login` - User login
- `/auth/register` - User registration
- `/auth/verify-email` - Email verification
- `/dashboard` - User dashboard
- `/listings` - Browse listings
- `/offers` - View offers
- `/chat` - Messaging
- `/wallet` - Wallet management

### API Gateway & Documentation

**Gateway Health**:

```
http://localhost:8080/health
```

**Service Documentation** (Swagger UI):

```
http://localhost:8080/api/auth/docs
http://localhost:8080/api/users/docs
http://localhost:8080/api/listings/docs
http://localhost:8080/api/offers/docs
http://localhost:8080/api/payments/docs
http://localhost:8080/api/chat/docs
http://localhost:8080/api/notifications/docs
```

### Direct Service Access (Development Only)

If needed, services can be accessed directly (bypassing Nginx):

```
Auth:         http://localhost:8000/docs
User:         http://localhost:8001/docs
Listing:      http://localhost:8002/docs
Offer:        http://localhost:8003/docs
Payment:      http://localhost:8004/docs
Admin:        http://localhost:8005/admin/
Chat:         http://localhost:8006/docs
Notification: http://localhost:8007/docs
```

---

## Monitoring & Logs

### View All Logs

```bash
# Follow logs in real-time
docker-compose logs -f

# View last 100 lines
docker-compose logs --tail=100
```

### View Specific Service Logs

```bash
docker-compose logs -f frontend
docker-compose logs -f auth
docker-compose logs -f nginx
docker-compose logs -f postgres
```

### Check Service Health

```bash
# Quick health check of all services
curl http://localhost:8080/health

# Check individual services
curl http://localhost:8000/health  # Auth
curl http://localhost:8001/health  # User
curl http://localhost:8002/health  # Listing
```

### Container Stats

```bash
# Monitor resource usage
docker stats

# Show running containers
docker ps

# Show all containers (including stopped)
docker ps -a
```

---

## Common Issues & Troubleshooting

### Issue: Port Already In Use

**Error**: `Error response from daemon: Bind for 0.0.0.0:3000 failed: port is already allocated`

**Solution**:

```bash
# Find what's using the port
lsof -i :3000

# Stop the conflicting service
kill -9 <PID>

# Or change the port in docker-compose.yml
# Change "3000:3000" to "3001:3000"
```

### Issue: Services Not Starting (Timeout)

**Error**: Services stuck in "starting" state

**Solution**:

```bash
# Stop and remove all containers
docker-compose down

# Remove volumes to reset databases
docker-compose down -v

# Start fresh
docker-compose up -d --build
```

### Issue: Frontend Can't Connect to Backend

**Error**: Frontend shows API errors or 404s

**Solution**:

```bash
# Verify Nginx is running
docker-compose logs nginx

# Verify backend services are healthy
docker-compose ps

# Test Nginx gateway directly
curl http://localhost:8080/api/auth/health

# Check frontend logs
docker-compose logs frontend
```

### Issue: Database Connection Failed

**Error**: Services show database connection errors

**Solution**:

```bash
# Check PostgreSQL is running
docker-compose logs postgres

# Restart database
docker-compose restart postgres

# Or reset completely
docker-compose down -v
docker-compose up -d
```

### Issue: Out of Memory

**Error**: Services crash with OOM error

**Solution**:

```bash
# Stop services
docker-compose down

# Increase Docker Desktop memory limit:
# - Windows: Docker Desktop Settings → Resources → Memory
# - Mac: Docker Desktop Settings → Resources → Memory
# - Linux: Adjust system memory

# Or reduce number of services by editing docker-compose.yml
```

---

## Stopping & Restarting Services

### Stop All Services (Keep Data)

```bash
docker-compose stop
```

### Stop All Services (Remove Data)

```bash
docker-compose down
```

### Restart Specific Service

```bash
docker-compose restart frontend
docker-compose restart auth
# etc.
```

### Rebuild Specific Service

```bash
docker-compose build frontend
docker-compose up -d frontend
```

### Rebuild All Services

```bash
docker-compose build
docker-compose up -d
```

---

## Database Management

### Access PostgreSQL CLI

```bash
# Connect to main database
docker-compose exec postgres psql -U swap_user -d auth

# List all databases
\l

# List tables in current database
\dt

# Exit
\q
```

### Reset Specific Database

```bash
# Stop services
docker-compose down

# Remove only volume
docker volume rm swap_postgres_data

# Restart
docker-compose up -d
```

### View Database Migrations

Migrations are handled by Alembic in each service. Check service documentation for migration commands.

---

## Development Workflow

### Code Changes (Hot Reload)

**Frontend** (Next.js dev mode):

1. Edit files in `frontend/src/`
2. Changes automatically reflected at http://localhost:3000
3. Check browser console for build errors

**Backend Services**:

1. Edit Python files in `services/{service}/`
2. Restart the service: `docker-compose restart {service}`
3. Check logs: `docker-compose logs {service}`

### Running Tests

```bash
# Run integration tests
bash tests/integration-tests.sh

# Run specific service tests
docker-compose exec auth pytest
docker-compose exec user pytest
```

### Debugging

**Frontend Debugging**:

- Open browser DevTools (F12)
- Check Network tab for API calls
- Check Console for errors

**Backend Debugging**:

- View logs: `docker-compose logs -f {service}`
- Add print statements and restart service
- Use FastAPI's `/docs` interface to test endpoints

---

## Performance Tuning

### Nginx Caching

- Listings: 15 minutes
- Users: 10 minutes
- Offers: 5 minutes
- Auth: No cache

### Nginx Rate Limiting

- General: 100 req/s per IP
- Auth: 10 req/s per IP
- Payment: 5 req/s per IP

### Database Connection Pooling

Configured in each service. Adjust as needed for load.

### Redis Caching

Used for session management and caching. Monitor with:

```bash
docker-compose exec redis redis-cli
> info
> keys *
```

---

## Production Deployment Notes

This docker-compose setup is for **development only**. For production:

1. **Security**:

   - Use environment variables for secrets (never commit credentials)
   - Enable HTTPS/SSL
   - Configure proper CORS policies
   - Implement rate limiting per user/API key

2. **Scaling**:

   - Use Kubernetes instead of docker-compose
   - Horizontal pod autoscaling
   - Database replication

3. **Monitoring**:

   - Add Prometheus + Grafana
   - Implement centralized logging (ELK stack)
   - Add distributed tracing (Jaeger)

4. **Database**:

   - Use managed PostgreSQL (AWS RDS, etc.)
   - Enable automated backups
   - Setup read replicas for scaling

5. **Infrastructure**:
   - Deploy to managed Kubernetes (EKS, GKE, AKS)
   - Use managed message queues (AWS SQS, Azure Service Bus)
   - Use managed storage (S3, Azure Blob Storage)

---

## Useful Commands Reference

```bash
# Status
docker-compose ps
docker-compose logs -f
docker stats

# Control
docker-compose up -d
docker-compose down
docker-compose restart
docker-compose stop
docker-compose start

# Building
docker-compose build
docker-compose build --no-cache
docker-compose up -d --build

# Debugging
docker-compose logs {service}
docker-compose exec {service} sh
docker-compose exec {service} bash

# Cleanup
docker-compose down -v
docker image prune -f
docker volume prune -f
docker container prune -f
```

---

## Support & Documentation

- **API Documentation**: See `INTEGRATION_TESTING_GUIDE.md`
- **Project Architecture**: See `README.md`
- **Frontend Code**: `frontend/src/`
- **Backend Services**: `services/*/`
- **Docker Setup**: `docker-compose.yml`, `nginx/nginx.conf`

For issues or questions, check the GitHub issues or project documentation.
