# 📦 Deployment Guide

## 🔗 GitHub Setup

### Prerequisites

- GitHub account
- Git installed locally
- SSH keys configured (or use HTTPS)

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Create repository: `swap` or `swap-platform`
3. **Do not** initialize with README (we already have one)
4. Copy the repository URL

### Step 2: Add Remote and Push

```bash
# Navigate to project
cd ~/Desktop/projects/swap

# Add remote origin (replace with your repo URL)
git remote add origin https://github.com/yourusername/swap.git

# Or use SSH
git remote add origin git@github.com:yourusername/swap.git

# Verify remote
git remote -v

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Verify on GitHub

Visit: https://github.com/yourusername/swap

You should see:

- ✅ 77 files committed
- ✅ README.md with project overview
- ✅ TEST_REPORT.md with test results
- ✅ All services and tests

---

## 🚀 Deployment Environments

### Local Development

```bash
docker compose up -d
```

Access: http://localhost:8000

### Staging

```bash
# Build and push Docker images to registry
docker build -t myregistry/swap-auth services/auth/
docker build -t myregistry/swap-offer services/offer/
docker build -t myregistry/swap-payment services/payment/

docker push myregistry/swap-auth
docker push myregistry/swap-offer
docker push myregistry/swap-payment

# Deploy with updated docker-compose
docker compose -f docker-compose.staging.yml up -d
```

### Production

1. Set up managed PostgreSQL instance
2. Configure Redis cluster
3. Set up managed Kafka (AWS MSK, Confluent Cloud, etc.)
4. Configure MinIO S3 bucket
5. Use Kubernetes or container orchestration:

```bash
# Example: Deploy to Kubernetes
kubectl create namespace swap
kubectl create configmap swap-config --from-literal=db_host=prod-db.rds.amazonaws.com
kubectl apply -f k8s/deployment.yaml -n swap
```

---

## 🔐 Environment Configuration

### Production .env

```
# Auth Service
AUTH_SECRET_KEY=your-production-secret-key-here
AUTH_ALGORITHM=HS256
AUTH_TOKEN_EXPIRE_MINUTES=30

# Database
DATABASE_URL=postgresql://user:password@prod-db.example.com:5432/swap_prod
REDIS_URL=redis://prod-redis.example.com:6379

# Kafka
KAFKA_BOOTSTRAP_SERVERS=prod-kafka.example.com:9092

# MinIO
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=your-secure-password
MINIO_ENDPOINT=s3.example.com

# Email
SMTP_SERVER=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USERNAME=apikey
SMTP_PASSWORD=your-sendgrid-key

# URLs
PUBLIC_URL=https://swap.example.com
FRONTEND_URL=https://app.swap.example.com
```

---

## 📊 Monitoring & Logging

### Application Monitoring

```bash
# Application Performance Monitoring (APM)
# Install NewRelic, DataDog, or similar

# Health checks
curl https://api.swap.example.com/health
```

### Log Aggregation

```bash
# Centralized logging with ELK Stack or Cloud Logging
# Ensure all container logs are forwarded to:
# - CloudWatch (AWS)
# - Stackdriver (GCP)
# - Azure Monitor
```

### Database Monitoring

```bash
# Enable query logging
# Monitor connections
# Set up backup strategies
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions

Create `.github/workflows/ci-cd.yml`:

```yaml
name: CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_DB: swap_test
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.12"
          cache: "pip"

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-asyncio httpx

      - name: Run tests
        run: pytest tests/ -v --cov=.

      - name: Upload coverage
        uses: codecov/codecov-action@v3

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'push'

    steps:
      - uses: actions/checkout@v3

      - name: Build Docker images
        run: |
          docker build -t ${{ secrets.REGISTRY }}/swap-auth:${{ github.sha }} services/auth/
          docker build -t ${{ secrets.REGISTRY }}/swap-offer:${{ github.sha }} services/offer/
          docker build -t ${{ secrets.REGISTRY }}/swap-payment:${{ github.sha }} services/payment/

      - name: Push to registry
        run: |
          echo ${{ secrets.REGISTRY_PASSWORD }} | docker login -u ${{ secrets.REGISTRY_USERNAME }} --password-stdin
          docker push ${{ secrets.REGISTRY }}/swap-auth:${{ github.sha }}
          docker push ${{ secrets.REGISTRY }}/swap-offer:${{ github.sha }}
          docker push ${{ secrets.REGISTRY }}/swap-payment:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
      - name: Deploy to production
        env:
          DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
        run: |
          ssh -i "$DEPLOY_KEY" deploy@api.swap.example.com \
            "cd /app && docker compose pull && docker compose up -d"
```

### GitHub Secrets Required

```
REGISTRY              # Docker registry URL
REGISTRY_USERNAME     # Registry username
REGISTRY_PASSWORD     # Registry password
DEPLOY_KEY           # SSH private key for production
```

---

## 📈 Scaling Considerations

### Horizontal Scaling

```bash
# Run multiple instances of each service
docker compose up -d --scale auth=3 --scale offer=2 --scale payment=2
```

### Load Balancing

```nginx
upstream auth_servers {
  server swap-auth-1:8000;
  server swap-auth-2:8000;
  server swap-auth-3:8000;
}

server {
  listen 80;
  location /auth {
    proxy_pass http://auth_servers;
  }
}
```

### Database Optimization

- Implement read replicas
- Use connection pooling (PgBouncer)
- Optimize queries with indices
- Archive old data

### Caching Strategy

- Redis for session storage
- Client-side caching headers
- CDN for static assets

---

## 🔐 Security Checklist

- [ ] Change default JWT secret in production
- [ ] Enable HTTPS/TLS on all endpoints
- [ ] Configure firewall rules
- [ ] Enable database encryption
- [ ] Set up Web Application Firewall (WAF)
- [ ] Enable API rate limiting
- [ ] Configure CORS properly
- [ ] Enable audit logging
- [ ] Regular security scanning
- [ ] Keep dependencies updated

---

## 📊 Performance Targets

- Auth registration: < 200ms
- Login: < 150ms
- Offer creation: < 300ms
- Payment processing: < 500ms
- Payment release: < 1s
- List offers: < 200ms

---

## 🚨 Rollback Procedures

```bash
# Rollback to previous version
git revert HEAD
docker compose pull
docker compose up -d

# Check logs
docker compose logs -f auth
```

---

## 📞 Support & Maintenance

### Scheduled Maintenance

- Database backups: Daily at 2 AM UTC
- Security updates: Monthly
- Major updates: Quarterly

### Incident Response

1. Alert team
2. Gather logs and metrics
3. Identify root cause
4. Apply fix
5. Test thoroughly
6. Deploy fix
7. Monitor
8. Retrospective

---

## 📚 Additional Resources

- Docker Compose Docs: https://docs.docker.com/compose/
- FastAPI Deployment: https://fastapi.tiangolo.com/deployment/
- PostgreSQL Production Guide: https://www.postgresql.org/docs/current/runtime.html
- Kubernetes Deployment: https://kubernetes.io/docs/

---

**Last Updated**: November 19, 2025
