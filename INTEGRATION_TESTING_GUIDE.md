# Frontend-Backend Integration Testing Guide

## Overview

This document describes how to test the Swap platform's frontend-backend integration through the Nginx API gateway.

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                         Frontend                              │
│                    http://localhost:3000                      │
│                    (Next.js 14 + TypeScript)                 │
└────────────┬─────────────────────────────────────────────────┘
             │
             │ HTTP Requests via axios
             │ (API Base: http://localhost:8080)
             │
┌────────────▼─────────────────────────────────────────────────┐
│                    Nginx API Gateway                          │
│                    http://localhost:8080                      │
│        Rate Limiting • Caching • CORS • Load Balancing      │
└──┬──┬──┬──┬──┬──┬──┬──┬──────────────────────────────────────┘
   │  │  │  │  │  │  │  │
   │  │  │  │  │  │  │  └─→ Notification (8007)
   │  │  │  │  │  │  └────→ Chat (8006)
   │  │  │  │  │  └───────→ Admin (8005)
   │  │  │  │  └──────────→ Payment (8004)
   │  │  │  └─────────────→ Offer (8003)
   │  │  └────────────────→ Listing (8002)
   │  └─────────────────→ User (8001)
   └──────────────────→ Auth (8000)

                    ┌──────────────┐
                    │ PostgreSQL   │ (8 databases)
                    │ Redis        │
                    │ Kafka        │
                    │ MinIO        │
                    └──────────────┘
```

## Running the Integration Tests

### 1. Start All Services

```bash
cd /path/to/swap
docker-compose up --build -d
```

This will start:

- ✅ PostgreSQL (with 8 separate databases)
- ✅ Redis
- ✅ Zookeeper & Kafka
- ✅ MinIO (S3-compatible storage)
- ✅ MailHog (email testing)
- ✅ Auth Service (8000)
- ✅ User Service (8001)
- ✅ Listing Service (8002)
- ✅ Offer Service (8003)
- ✅ Payment Service (8004)
- ✅ Admin Service (8005)
- ✅ Chat Service (8006)
- ✅ Notification Service (8007)
- ✅ Nginx Gateway (8080)
- ✅ Frontend (3000)

### 2. Verify Services Are Healthy

```bash
# Check all services
docker-compose ps

# Expected output should show all services as "Up"
```

### 3. Run Integration Tests

```bash
# Run the integration test suite
bash tests/integration-tests.sh

# Or manually test endpoints
curl http://localhost:8080/health
curl http://localhost:8080/api/auth/health
curl http://localhost:3000/
```

## Testing Workflow

### 1. Test Health Endpoints

All services have a `/health` endpoint for health checks:

```bash
# Test Nginx gateway
curl http://localhost:8080/health

# Test individual services through nginx
curl http://localhost:8080/api/auth/health
curl http://localhost:8080/api/users/health
curl http://localhost:8080/api/listings/health
curl http://localhost:8080/api/offers/health
curl http://localhost:8080/api/payments/health
curl http://localhost:8080/api/chat/health
curl http://localhost:8080/api/notifications/health
```

### 2. Access API Documentation

Each service has Swagger documentation at `/docs`:

```
Auth:         http://localhost:8080/api/auth/docs
Users:        http://localhost:8080/api/users/docs
Listings:     http://localhost:8080/api/listings/docs
Offers:       http://localhost:8080/api/offers/docs
Payments:     http://localhost:8080/api/payments/docs
Chat:         http://localhost:8080/api/chat/docs
Notifications: http://localhost:8080/api/notifications/docs
Admin:        http://localhost:8005/admin/ (Direct, not through nginx)
```

### 3. Test Frontend

Open in browser:

```
http://localhost:3000/
```

Navigate through:

- `/auth/login` - Test login form
- `/auth/register` - Test registration
- `/dashboard` - Test dashboard page
- `/listings` - Test listings browse page
- `/offers` - Test offers page
- `/chat` - Test messaging page
- `/wallet` - Test wallet management

### 4. Test API Calls Through Frontend

The frontend makes API calls to `http://localhost:8080` through the Nginx gateway.

#### Example: Authentication Flow

1. **Register** (POST /api/auth/register)

```bash
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!",
    "username": "testuser"
  }'
```

2. **Login** (POST /api/auth/login)

```bash
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!"
  }'
```

3. **Get Profile** (GET /api/auth/profile)

```bash
curl http://localhost:8080/api/auth/profile \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Frontend Configuration

The frontend is configured in `.env` to use the Nginx gateway:

```env
NEXT_PUBLIC_API_URL=http://localhost:8080
NEXT_PUBLIC_SOCKET_URL=ws://localhost:8080
```

This means all API calls from the frontend will go through:

- `http://localhost:8080/api/auth/*`
- `http://localhost:8080/api/users/*`
- `http://localhost:8080/api/listings/*`
- etc.

## API Client Integration

The frontend uses an Axios-based API client (`@/lib/api-client.ts`) that:

1. ✅ Automatically includes JWT tokens in requests
2. ✅ Handles 401 unauthorized responses by redirecting to login
3. ✅ Provides strongly-typed API methods for all services
4. ✅ Includes request/response interceptors

### API Service Methods Available

```typescript
// Authentication
authApi.register({ email, password, username });
authApi.login({ email, password });
authApi.logout();
authApi.verifyEmail(token);
authApi.refreshToken();

// Users
userApi.getUser(id);
userApi.getProfile();
userApi.updateProfile(data);
userApi.getWallet();

// Listings
listingApi.getListings(filters);
listingApi.getListing(id);
listingApi.createListing(data);
listingApi.searchListings(query);

// Offers
offerApi.getOffers(filters);
offerApi.createOffer(data);
offerApi.updateOfferStatus(id, status);

// Payments
paymentApi.createPayment(data);
paymentApi.getPaymentHistory();
paymentApi.releaseEscrow(offerId);

// Chat
chatApi.getConversations();
chatApi.sendMessage(conversationId, message);

// Notifications
notificationApi.getNotifications();
notificationApi.markAsRead(id);
```

## Testing Checklist

### Frontend Pages

- [ ] Login page loads (`/auth/login`)
- [ ] Register page loads (`/auth/register`)
- [ ] Email verification page loads (`/auth/verify-email`)
- [ ] Dashboard page loads (`/dashboard`)
- [ ] Listings page loads (`/listings`) with filters working
- [ ] Offers page loads (`/offers`)
- [ ] Chat page loads (`/chat`)
- [ ] Wallet page loads (`/wallet`)

### API Connectivity

- [ ] Nginx gateway responds at `http://localhost:8080/health`
- [ ] Auth service accessible through gateway
- [ ] User service accessible through gateway
- [ ] Listing service accessible through gateway
- [ ] Offer service accessible through gateway
- [ ] Payment service accessible through gateway
- [ ] Chat service accessible through gateway
- [ ] Notification service accessible through gateway

### Full Flow Integration

- [ ] User can register through frontend
- [ ] User can login through frontend
- [ ] User can view dashboard
- [ ] User can browse listings
- [ ] User can create/view offers
- [ ] User can access wallet
- [ ] All form submissions work without errors
- [ ] Error messages display properly
- [ ] Loading states show correctly

## Debugging

### Check Service Logs

```bash
# Auth service
docker-compose logs auth

# Frontend
docker-compose logs frontend

# Nginx
docker-compose logs nginx

# All services
docker-compose logs -f
```

### Test Individual Services Directly (Not Through Nginx)

```bash
# Connect directly to auth service (bypass nginx)
curl http://localhost:8000/health

# Connect directly to user service
curl http://localhost:8001/health
```

### Test Nginx Routing

```bash
# Check if nginx is correctly routing to backend services
curl -v http://localhost:8080/api/auth/health
# Look for X-Real-IP, X-Forwarded-For headers
```

## Common Issues

### Issue: Frontend can't connect to backend

**Solution**: Check that `NEXT_PUBLIC_API_URL` is set to `http://localhost:8080` in docker-compose environment.

### Issue: CORS errors

**Solution**: Nginx has CORS headers configured. Check that they're being sent:

```bash
curl -i http://localhost:8080/api/auth/health
# Look for Access-Control-Allow-* headers
```

### Issue: 502 Bad Gateway errors

**Solution**: Check that backend services are running:

```bash
docker-compose ps
# All services should show "Up"
```

### Issue: Frontend page shows blank/errors

**Solution**: Check frontend logs:

```bash
docker-compose logs frontend
```

## Performance Considerations

1. **Rate Limiting** (via Nginx):

   - General endpoints: 100 req/s per IP
   - Auth endpoints: 10 req/s per IP (strict)
   - Payment endpoints: 5 req/s per IP (very strict)

2. **Caching** (via Nginx):

   - Listings: 15 minutes
   - Users: 10 minutes
   - Offers: 5 minutes
   - Auth: No cache

3. **Client Timeout Settings**:
   - Request: 60 seconds
   - Script: 5 seconds
   - WebSocket: 86400 seconds (24 hours)

## Next Steps

After successful integration testing:

1. Run end-to-end tests with Cypress or Playwright
2. Load test the system with k6 or Apache JMeter
3. Security test with OWASP ZAP
4. Performance profiling with Chrome DevTools

See the main README.md for more details on the project architecture.
