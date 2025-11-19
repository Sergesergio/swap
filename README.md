# 🔄 Swap Platform - Digital & Tangible Asset Exchange

A microservices-based platform enabling secure asset swaps, sales, and purchases with multi-party support, escrow payments, and real-time communication.

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.12+ (for local development)
- Git

### Start the Platform

```bash
# Clone repository
git clone https://github.com/yourusername/swap.git
cd swap

# Start all services
docker compose up -d

# Seed dummy data (optional)
python scripts/seed_dummy_data.py

# Run tests
python -m pytest tests/ -v
```

### Access Services

| Service      | URL                   | Purpose                            |
| ------------ | --------------------- | ---------------------------------- |
| Auth         | http://localhost:8000 | User registration & authentication |
| User         | http://localhost:8001 | User profiles & wallets            |
| Listing      | http://localhost:8002 | Item listings & categories         |
| Offer        | http://localhost:8003 | Swap proposals & negotiations      |
| Payment      | http://localhost:8004 | Escrow & transactions              |
| Chat         | http://localhost:8005 | Real-time messaging                |
| Notification | http://localhost:8006 | Multi-channel alerts               |
| Admin        | http://localhost:8007 | Moderation & disputes              |

### API Documentation

- **Swagger UI**: http://localhost:8000/docs (and each service)
- **ReDoc**: http://localhost:8000/redoc

---

## 📊 Architecture

### Microservices Structure

```
swap/
├── services/
│   ├── auth/          # JWT authentication & user management
│   ├── user/          # User profiles, ratings, wallets
│   ├── listing/       # Item listings & categories
│   ├── offer/         # Swap proposals & negotiations
│   ├── payment/       # Escrow & transaction processing
│   ├── chat/          # WebSocket messaging
│   ├── notification/  # Email, SMS, push notifications
│   └── admin/         # Moderation & dispute resolution
├── shared/            # Common models, exceptions, auth
├── scripts/           # Utilities (seeding, migrations)
├── tests/             # Test suites
└── docker-compose.yml # Multi-service orchestration
```

### Tech Stack

- **Language**: Python 3.12
- **Framework**: FastAPI
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **Event Bus**: Apache Kafka 7.3
- **File Storage**: MinIO (S3-compatible)
- **Testing**: Pytest + HTTPx
- **Containerization**: Docker & Docker Compose

---

## 🔐 Authentication

### Register New User

```bash
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "username",
    "password": "SecurePass123!"
  }'
```

### Login

```bash
curl -X POST http://localhost:8000/token \
  -d "username=user@example.com&password=SecurePass123!"
```

### Response

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### Use Token

```bash
curl -X GET http://localhost:8000/me \
  -H "Authorization: Bearer {access_token}"
```

---

## 💼 Workflow Examples

### Complete Swap Transaction

#### 1. Register Users

```bash
# Buyer
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{"email":"buyer@example.com","username":"buyer","password":"Pass123!"}'

# Seller
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{"email":"seller@example.com","username":"seller","password":"Pass123!"}'
```

#### 2. Seller Creates Listing

```bash
curl -X POST http://localhost:8002/api/v1/listings/ \
  -H "Authorization: Bearer {seller_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "iPhone 12 Pro",
    "description": "Great condition",
    "category": "electronics",
    "condition": "excellent",
    "price": 800.0
  }'
```

#### 3. Buyer Creates Offer

```bash
curl -X POST http://localhost:8003/api/v1/offers/ \
  -H "Authorization: Bearer {buyer_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "listing_id": 1,
    "type": "direct_buy",
    "price": 750.0,
    "message": "Can you accept $750?"
  }'
```

#### 4. Seller Accepts Offer

```bash
curl -X POST http://localhost:8003/api/v1/offers/1/accept \
  -H "Authorization: Bearer {seller_token}"
```

#### 5. Process Payment

```bash
curl -X POST http://localhost:8004/api/v1/payments/hold \
  -H "Authorization: Bearer {buyer_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "offer_id": 1,
    "amount": 750.0,
    "payment_method": "credit_card"
  }'
```

#### 6. Release Payment to Seller

```bash
curl -X POST http://localhost:8004/api/v1/payments/1/release \
  -H "Authorization: Bearer {admin_token}"
```

---

## 🧪 Testing

### Run All Tests

```bash
pytest tests/ -v
```

### Run Specific Test Suite

```bash
# Auth tests
pytest tests/test_auth_unit.py -v

# Offer & Payment tests
pytest tests/test_offer_payment_unit.py -v

# Integration tests
pytest tests/test_integration.py -v

# End-to-end tests
pytest tests/test_e2e.py -v
```

### Test Coverage

```bash
pytest tests/ --cov=. --cov-report=html
```

### Test Report

See [TEST_REPORT.md](TEST_REPORT.md) for detailed results:

- ✅ 19 tests passing
- ⏳ 14 tests skipped
- Status: Platform operational, core auth functional

---

## 📝 Test Users (Seeded Data)

| Email               | Username        | Password          | Role   |
| ------------------- | --------------- | ----------------- | ------ |
| alice@example.com   | alice_smith     | AliceSecure123!   | Buyer  |
| bob@example.com     | bob_seller      | BobSecure123!     | Seller |
| charlie@example.com | charlie_trader  | CharlieSecure123! | Both   |
| diana@example.com   | diana_collector | DianaSecure123!   | Buyer  |
| eve@example.com     | eve_merchant    | EveSecure123!     | Seller |

### Sample Listings

- Vintage Leather Jacket ($150)
- iPhone 12 Pro Max ($800)
- Antique Wooden Desk ($350)
- Samsung 4K TV ($450)
- Mountain Bike ($600)
- MacBook Pro 2019 ($900)
- Gold Diamond Ring ($2,500)
- Acoustic Guitar ($250)

---

## 🛠️ Development

### Local Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install pytest pytest-asyncio httpx black isort mypy
```

### Code Quality

```bash
# Format code
black . && isort .

# Lint
flake8 .

# Type checking
mypy services/
```

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head
```

### View Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f auth
```

---

## 📚 API Reference

### Authentication Endpoints

| Method | Path        | Description              |
| ------ | ----------- | ------------------------ |
| POST   | `/register` | Register new user        |
| POST   | `/token`    | Login (get access token) |
| POST   | `/refresh`  | Refresh access token     |
| GET    | `/me`       | Get current user profile |

### Offer Endpoints

| Method | Path                            | Description       |
| ------ | ------------------------------- | ----------------- |
| POST   | `/api/v1/offers/`               | Create new offer  |
| GET    | `/api/v1/offers/{id}`           | Get offer details |
| POST   | `/api/v1/offers/{id}/accept`    | Accept offer      |
| POST   | `/api/v1/offers/{id}/reject`    | Reject offer      |
| POST   | `/api/v1/offers/{id}/messages/` | Add message       |
| GET    | `/api/v1/offers/{id}/messages/` | Get messages      |
| GET    | `/api/v1/offers/user/{user_id}` | Get user offers   |

### Payment Endpoints

| Method | Path                              | Description           |
| ------ | --------------------------------- | --------------------- |
| POST   | `/api/v1/payments/hold`           | Hold payment (escrow) |
| POST   | `/api/v1/payments/{id}/release`   | Release held payment  |
| POST   | `/api/v1/payments/{id}/refund`    | Refund payment        |
| GET    | `/api/v1/payments/{id}`           | Get payment details   |
| GET    | `/api/v1/payments/user/{user_id}` | Get user payments     |

---

## 🔄 Event Flow (Kafka Topics)

- `user.created` - New user registered
- `listing.created` - New item listed
- `offer.created` - Offer submitted
- `offer.accepted` - Offer accepted by seller
- `payment.held` - Payment escrowed
- `payment.released` - Payment sent to seller
- `notification.send` - Send notification

---

## 🐛 Troubleshooting

### Service Won't Start

```bash
# Check logs
docker compose logs {service}

# Rebuild service
docker compose build --no-cache {service}

# Restart all services
docker compose restart
```

### Database Connection Error

```bash
# Verify PostgreSQL is running
docker compose ps postgres

# Reset database
docker compose exec postgres psql -U postgres -c "DROP DATABASE swap_db; CREATE DATABASE swap_db;"
```

### Port Already in Use

```bash
# Find what's using the port
lsof -i :8000

# Or change ports in docker-compose.yml
```

### Test Failures

```bash
# Ensure services are running
docker compose up -d

# Clear test cache
rm -rf .pytest_cache

# Run with verbose output
pytest tests/ -v -s
```

---

## 📊 Monitoring

### Health Checks

```bash
# All services
curl http://localhost:8000/health
curl http://localhost:8001/health
curl http://localhost:8002/health
curl http://localhost:8003/health
curl http://localhost:8004/health
```

### Database

```bash
# Connect to PostgreSQL
docker compose exec postgres psql -U postgres -d swap_db

# Check tables
\dt

# View users
SELECT id, email, username FROM users;
```

### Redis Cache

```bash
# Connect to Redis
docker compose exec redis redis-cli

# Check keys
KEYS *

# View memory usage
INFO memory
```

---

## 🤝 Contributing

1. Fork repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push branch: `git push origin feature/amazing-feature`
5. Open Pull Request

### Code Style

- Python: PEP 8 (enforced with black/isort)
- Type hints for all functions
- Docstrings for modules, classes, methods
- Tests for new features

---

## 📄 License

MIT License - see LICENSE file

---

## 👥 Authors

- **Serge** - Initial development

---

## 📞 Support

- **Issues**: GitHub Issues
- **Documentation**: See `/docs` or http://localhost:8000/docs
- **Email**: serge@example.com

---

## 🗺️ Project Status

- ✅ Core services: Auth, Offer, Payment
- 🔄 User service: In progress
- 🔄 Listing service: In progress
- 📋 Chat service: Planned
- 📋 Notification service: Planned
- 📋 Admin service: Planned

**Current Version**: 0.1.0 (Alpha)  
**Last Updated**: November 19, 2025
