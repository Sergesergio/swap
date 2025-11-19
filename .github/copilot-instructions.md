# AI Agent Instructions for Swap Platform

## Project Overview

Swap is a digital and tangible asset exchange platform built on a microservices architecture. The platform enables users to swap, sell, or buy items with secure escrow payments and multi-party swap capabilities.

### Tech Stack

- Language: Python 3.12
- Framework: FastAPI with Pydantic
- Database: PostgreSQL with SQLModel ORM
- Cache/Queue: Redis
- Event Bus: Apache Kafka
- Storage: MinIO (S3-compatible)
- Containerization: Docker & Docker Compose
- Auth: JWT with refresh tokens (cookies)
- Testing: Pytest + HTTPX

## Architecture Overview

### Microservices Structure

Each microservice follows Clean Architecture pattern with the following structure:

```
/services/{service_name}/
├── main.py           # FastAPI entrypoint
├── models.py         # SQLModel definitions
├── repository/       # Database operations
├── routers/         # API endpoints
├── events/          # Kafka producers/consumers
└── Dockerfile
```

### Core Services

1. Auth Service (`/services/auth/`) - Authentication, JWT management
2. User Service (`/services/user/`) - Profiles, ratings, wallets
3. Listing Service (`/services/listing/`) - Item listings, categories
4. Offer Service (`/services/offer/`) - Swap proposals, negotiations
5. Payment Service (`/services/payment/`) - Escrow, transactions
6. Notification Service (`/services/notification/`) - Multi-channel notifications
7. Chat Service (`/services/chat/`) - WebSocket-based messaging
8. Admin Service (`/services/admin/`) - Moderation, disputes

## Key Development Patterns

### Service Independence

- Each service has its own database/schema
- Services communicate via REST (sync) or Kafka (async)
- Independent Swagger docs at `/docs` per service
- Health checks at `/health`

### Event-Driven Communication

Standard Kafka topics:

- `user.created`
- `listing.created`
- `offer.created`
- `payment.held`
- `payment.released`
- `notification.send`

### Authentication & Security

- JWT stored in HTTP-only cookies
- Refresh token rotation
- Role-based access: user, verified_seller, admin
- Environment variables in service-specific .env files

### Database Patterns

- Use SQLModel for type-safe ORM
- Migrations handled by Alembic
- Repository pattern for DB operations
- Soft deletes where applicable

## Development Workflows

### Local Development

1. Start all services:

   ```bash
   docker-compose up --build
   ```

2. Run tests:

   ```bash
   docker-compose -f docker-compose.test.yml up --build --exit-code-from tests
   ```

3. Access service docs:
   - Auth: http://localhost:8000/docs
   - User: http://localhost:8001/docs
   - Listing: http://localhost:8002/docs
     (etc. for each service)

### Adding New Features

1. Identify target service(s)
2. Update models in `models.py`
3. Add repository methods
4. Implement API endpoints in `routers/`
5. Add Kafka events if needed
6. Write tests in `tests/`

### Testing Guidelines

- Unit tests for all routes and services
- Integration tests for Kafka flows
- Use pytest fixtures for test data
- Mock external services appropriately

## Integration Points

### Inter-Service Communication

- Use `HTTPXClient` for REST calls
- Kafka for async events
- Circuit breakers for resilience

### External Services

- MinIO for file storage
- Redis for caching/rate limiting
- SMTP/FCM for notifications

## Common Gotchas & Tips

- Always use dependency injection for services
- Handle Kafka consumer group IDs carefully
- Check transaction isolation levels for payment ops
- Use background tasks for long-running operations

## Project Status

Initial development phase - core services being established.

---

Note: These instructions reflect the current state and will be updated as the project evolves.
