# Swap Platform - Quick Start Guide

## Installation & Setup

### Prerequisites

- Docker & Docker Compose
- Python 3.12+ (for local development)
- PostgreSQL client (optional, for debugging)

### Step 1: Clone and Setup

```bash
cd ~/Desktop/projects/swap
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate.ps1
pip install -r requirements.txt
```

### Step 2: Start Infrastructure

```bash
# Start all services (creates containers and starts services)
docker-compose up --build

# In another terminal, verify services are running
curl http://localhost:8000/health  # Auth service
curl http://localhost:8003/health  # Offer service
curl http://localhost:8004/health  # Payment service
```

## Service URLs

| Service     | Port | Docs                       | Health                       |
| ----------- | ---- | -------------------------- | ---------------------------- |
| Auth        | 8000 | http://localhost:8000/docs | http://localhost:8000/health |
| User        | 8001 | http://localhost:8001/docs | http://localhost:8001/health |
| Listing     | 8002 | http://localhost:8002/docs | http://localhost:8002/health |
| **Offer**   | 8003 | http://localhost:8003/docs | http://localhost:8003/health |
| **Payment** | 8004 | http://localhost:8004/docs | http://localhost:8004/health |

## Complete Workflow Example

### 1. Create a Listing

```bash
curl -X POST http://localhost:8002/api/v1/listings/ \
  -H "Content-Type: application/json" \
  -H "X-User-Id: 2" \
  -d '{
    "title": "Vintage Camera",
    "description": "Classic 35mm film camera",
    "category": "electronics",
    "price": 150.0
  }'
# Response: { "id": 1, ... }
```

### 2. Create an Offer (as buyer)

```bash
curl -X POST http://localhost:8003/api/v1/offers/ \
  -H "Content-Type: application/json" \
  -H "X-User-Id: 1" \
  -d '{
    "listing_id": 1,
    "buyer_id": 1,
    "seller_id": 2,
    "type": "direct_buy",
    "price": 150.0,
    "message": "I would like to buy this camera"
  }'
# Response: { "id": 1, "status": "pending", ... }
```

### 3. Accept Offer (as seller)

```bash
curl -X POST http://localhost:8003/api/v1/offers/1/accept \
  -H "X-User-Id: 2"
# Response: { "id": 1, "status": "accepted", ... }
# This triggers payment.hold_request event
```

### 4. Hold Payment (automatic via event)

Payment service consumes the event and creates a payment hold:

```bash
# View payment status
curl http://localhost:8004/api/v1/payments/1 \
  -H "X-User-Id: 1"
# Response: { "id": 1, "status": "held", "amount": 150.0, ... }
```

### 5. Release Payment (completes transaction)

```bash
curl -X POST http://localhost:8004/api/v1/payments/1/release \
  -H "X-User-Id: 1"
# Response: { "id": 1, "status": "released", ... }
# This triggers payment.released event, completing the offer
```

## Testing

### Run All Tests

```bash
# Using docker-compose (recommended)
docker-compose -f docker-compose.test.yml up --build --exit-code-from tests

# Or locally with pytest (requires PostgreSQL running)
pytest tests/ -v
```

### Run Specific Test

```bash
pytest tests/test_integration.py::test_create_offer -v
```

### Generate Coverage Report

```bash
pytest tests/ --cov=services --cov-report=html
open htmlcov/index.html  # View report
```

## Development Tips

### View Service Logs

```bash
# Watch all services
docker-compose logs -f

# Watch specific service
docker-compose logs -f offer
docker-compose logs -f payment
```

### Access Database

```bash
# Connect to PostgreSQL
psql -h localhost -U swap_user -d swap

# List tables
\dt  # in psql

# View offers
SELECT * FROM offers;
SELECT * FROM payments;
```

### View Kafka Events

```bash
# Get into Kafka container
docker exec -it swap_kafka_1 bash

# List topics
kafka-topics --bootstrap-server localhost:9092 --list

# Consume events (start from beginning)
kafka-console-consumer --bootstrap-server localhost:9092 --topic offer.created --from-beginning
kafka-console-consumer --bootstrap-server localhost:9092 --topic payment.held --from-beginning
```

### View MinIO/S3

Open http://localhost:9001 in browser

- Username: `minioadmin`
- Password: `minioadmin`

## Authentication

For local development, use simple header-based auth:

### Option 1: User ID Header

```bash
curl -X GET http://localhost:8003/api/v1/offers/user/1 \
  -H "X-User-Id: 1"
```

### Option 2: Bearer Token Format

```bash
curl -X GET http://localhost:8003/api/v1/offers/user/1 \
  -H "Authorization: Bearer user:1"
```

## Code Structure

### Adding a New Service

1. Create `services/{service_name}/` directory
2. Add `models.py` with SQLModel definitions
3. Add `repository/` with database operations
4. Add `routers/` with FastAPI endpoints
5. Add `events/producer.py` and `consumer.py` for Kafka
6. Create `main.py` with FastAPI app setup
7. Add `Dockerfile`
8. Update `docker-compose.yml`

### Adding a New Endpoint

1. Define request/response models in `services/{service}/models.py`
2. Add route handler in `services/{service}/routers/{module}.py`
3. Use `Depends(get_session)` for database access
4. Use `Depends(get_current_user)` for auth
5. Test with `pytest` or curl

## Troubleshooting

### Port Already in Use

```bash
# Find and kill process using port
lsof -i :8003
kill -9 <PID>
```

### Database Connection Error

```bash
# Ensure PostgreSQL is running
docker-compose ps postgres

# Restart PostgreSQL
docker-compose restart postgres
```

### Kafka Events Not Processing

```bash
# Check if Kafka is running
docker-compose ps kafka

# View Kafka logs
docker-compose logs kafka

# Restart Kafka
docker-compose restart kafka
```

### Offers Not Triggering Payments

1. Verify Kafka is running: `docker-compose logs kafka`
2. Check payment service consumer logs: `docker-compose logs payment`
3. Verify databases are created: `docker-compose exec postgres psql -U swap_user -d swap -c "\dt"`

## Performance & Scaling

### Local Optimization

- Redis caching available at `redis://redis:6379`
- Connection pooling configured in SQLModel
- Async Kafka producers for non-blocking operations

### Production Deployment

- Use environment variables for database URLs
- Enable HTTPS/TLS for all services
- Configure rate limiting (CORS + custom middleware)
- Add request logging and monitoring
- Deploy with Kubernetes or Docker Swarm
- Set up CI/CD pipeline with GitHub Actions

## API Documentation

Each service has auto-generated Swagger docs:

- http://localhost:8003/docs (Offer API)
- http://localhost:8004/docs (Payment API)

Click "Try it out" on any endpoint to test directly from the browser.

## Support & Debugging

### Enable Debug Logging

```bash
# In docker-compose.yml, add to services:
environment:
  - LOG_LEVEL=DEBUG
```

### View Request/Response

```bash
# Install httpie for better formatting
pip install httpie

# Use instead of curl
http POST http://localhost:8003/api/v1/offers/ \
  X-User-Id:1 \
  listing_id=1 \
  buyer_id=1 \
  seller_id=2 \
  type=direct_buy \
  price=100
```

---

**Happy developing! 🚀**
