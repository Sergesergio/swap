# Swap Platform - Quick Reference Card

## 🚀 One-Minute Start

```bash
cd /path/to/swap
docker-compose up -d --build
# Wait 2-3 minutes for all services to start
```

Then open:
- **App**: http://localhost:3000/
- **API**: http://localhost:8080/health
- **Docs**: http://localhost:8080/api/auth/docs

---

## 📁 Key Files & Directories

| Path | Purpose |
|------|---------|
| `frontend/src/app/` | 8 Main pages |
| `frontend/src/lib/api-client.ts` | API configuration |
| `frontend/src/stores/` | State management |
| `services/*/` | 8 Microservices |
| `nginx/nginx.conf` | API gateway routing |
| `docker-compose.yml` | Service orchestration |
| `cypress/e2e/` | E2E tests (58+ cases) |
| `DEPLOYMENT_GUIDE.md` | Operations guide |
| `E2E_TESTING_GUIDE.md` | Test framework |
| `PROJECT_COMPLETION_SUMMARY.md` | Full overview |

---

## 📋 Available Pages

```
http://localhost:3000/auth/login              - User login
http://localhost:3000/auth/register           - Registration
http://localhost:3000/auth/verify-email       - Email verification
http://localhost:3000/dashboard               - User dashboard
http://localhost:3000/listings                - Browse listings
http://localhost:3000/offers                  - Manage offers
http://localhost:3000/chat                    - Messaging
http://localhost:3000/wallet                  - Wallet management
```

---

## 🔌 API Endpoints (via Gateway)

```
Auth:         http://localhost:8080/api/auth/health
Users:        http://localhost:8080/api/users/health
Listings:     http://localhost:8080/api/listings/health
Offers:       http://localhost:8080/api/offers/health
Payments:     http://localhost:8080/api/payments/health
Chat:         http://localhost:8080/api/chat/health
Notifications: http://localhost:8080/api/notifications/health
```

---

## 🧪 Testing Commands

```bash
# Install Cypress (if not done)
npm install --save-dev cypress

# Open interactive test runner
npm run test:open

# Run all tests headless
npm run test

# Run specific feature
npm run test:auth        # Authentication
npm run test:listings    # Listings
npm run test:offers      # Offers
npm run test:chat        # Chat
npm run test:wallet      # Wallet
```

---

## 🐳 Docker Commands

```bash
# Status
docker-compose ps

# Logs
docker-compose logs -f                    # All services
docker-compose logs -f frontend           # Specific service

# Control
docker-compose up -d                      # Start all
docker-compose down                       # Stop all
docker-compose restart frontend           # Restart one
docker-compose build frontend             # Rebuild one

# Cleanup
docker-compose down -v                    # Stop + remove volumes
docker image prune -f                     # Clean dangling images
```

---

## 🔍 Debugging

```bash
# Check service logs
docker-compose logs frontend
docker-compose logs auth
docker-compose logs nginx

# Access service shell
docker-compose exec frontend sh
docker-compose exec postgres psql -U swap_user -d auth

# Test endpoints
curl http://localhost:8080/health
curl http://localhost:8080/api/auth/health

# Monitor resources
docker stats
```

---

## 📚 Documentation

| Document | Content |
|----------|---------|
| `DEPLOYMENT_GUIDE.md` | How to run and operate all services |
| `INTEGRATION_TESTING_GUIDE.md` | How to test APIs manually |
| `E2E_TESTING_GUIDE.md` | How to write and run E2E tests |
| `PROJECT_COMPLETION_SUMMARY.md` | Complete project overview |
| `README.md` | Architecture and getting started |

---

## 🛠️ Development Workflow

### Frontend Changes (Hot Reload)
1. Edit files in `frontend/src/`
2. Changes auto-reload at http://localhost:3000/
3. Check browser console for errors

### Backend Changes
1. Edit files in `services/{service}/`
2. Restart service: `docker-compose restart {service}`
3. View logs: `docker-compose logs {service}`

### Adding Tests
1. Create test in `cypress/e2e/*.cy.ts`
2. Add data-testid to components you're testing
3. Run tests: `npm run test:open`

---

## ✅ Service Status Checklist

- [ ] PostgreSQL healthy (check `docker-compose ps`)
- [ ] All services showing "Up" status
- [ ] Frontend accessible at :3000
- [ ] API gateway responding at :8080
- [ ] No 502 Bad Gateway errors
- [ ] Logs show no critical errors

---

## 🎯 Common Tasks

### Want to...
- **Start fresh**: `docker-compose down -v && docker-compose up -d --build`
- **View frontend code**: `frontend/src/app/`
- **Check API docs**: `http://localhost:8080/api/auth/docs`
- **Run tests**: `npm run test:open` or `npm run test`
- **Monitor services**: `docker stats` or `docker-compose logs -f`
- **Reset database**: `docker-compose down -v`
- **Add new page**: Create folder in `frontend/src/app/` with `page.tsx`
- **Add new test**: Create file in `cypress/e2e/` following existing pattern

---

## 🚨 Common Issues

| Issue | Solution |
|-------|----------|
| Port in use | Kill process on port: `lsof -i :3000` then `kill -9 <PID>` |
| Services won't start | `docker-compose down -v && docker-compose up -d --build` |
| Can't connect to backend | Check nginx running: `docker-compose logs nginx` |
| Out of memory | Increase Docker memory in settings |
| Database errors | Restart postgres: `docker-compose restart postgres` |
| Tests timing out | Check if services running: `docker-compose ps` |

---

## 📊 Architecture at a Glance

```
FRONTEND (:3000)
    ↓ (HTTP)
NGINX GATEWAY (:8080)
    ↓ (Routes)
[Auth] [User] [Listing] [Offer]
[Payment] [Chat] [Notification] [Admin]
    ↓ (Data)
PostgreSQL + Redis + Kafka + MinIO
```

---

## 🎓 Learning Resources

- Frontend: `frontend/src/` (React/TypeScript)
- API Integration: `frontend/src/lib/api-client.ts`
- Testing: `cypress/e2e/` (Cypress tests)
- Docker: `docker-compose.yml`
- Nginx: `nginx/nginx.conf`

---

## 📞 Need Help?

1. Check relevant documentation:
   - Ops: `DEPLOYMENT_GUIDE.md`
   - Testing: `E2E_TESTING_GUIDE.md` or `INTEGRATION_TESTING_GUIDE.md`
   - Overview: `PROJECT_COMPLETION_SUMMARY.md`

2. View logs: `docker-compose logs {service}`

3. Check status: `docker-compose ps`

4. Reset everything: `docker-compose down -v && docker-compose up -d --build`

---

## ✨ Features Available

### Frontend Pages
- ✅ Authentication (Login, Register, Email Verification)
- ✅ Dashboard (Stats, quick actions)
- ✅ Listings (Browse, search, filter)
- ✅ Offers (Create, negotiate, manage)
- ✅ Chat (Real-time messaging)
- ✅ Wallet (Balance, topup, withdraw)

### Quality Features
- ✅ Dark mode support
- ✅ Responsive design (mobile, tablet, desktop)
- ✅ Form validation with error messages
- ✅ Loading states
- ✅ Error handling
- ✅ Type-safe TypeScript
- ✅ Zustand state management

### Testing
- ✅ 58+ E2E test cases
- ✅ 5 feature test suites
- ✅ Cypress interactive testing
- ✅ Headless CI/CD ready

---

**Last Updated**: December 3, 2025
**Status**: ✅ COMPLETE AND READY FOR USE
