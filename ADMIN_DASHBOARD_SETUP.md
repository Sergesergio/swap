# Admin Dashboard Setup & Troubleshooting Guide

## Quick Start ✅

### Admin Dashboard Access

- **URL**: http://localhost:8005/admin/
- **Username**: `admin`
- **Password**: `AdminSwap123!`

---

## Connection Issues & Solutions

### Issue 1: "Unable to Connect" Error

**Problem**: Browser shows "Unable to connect" when trying to access http://localhost:8005/admin/

**Solution Steps**:

1. **Verify Docker is Running**

   ```powershell
   docker ps | Select-Object -First 5
   ```

   Look for `swap-admin-1` in the list. If it's not there, go to Step 2.

2. **Start the Admin Service**

   ```powershell
   cd "c:\Users\Trendig Biz&Tech\Desktop\projects\swap"
   docker compose up -d admin
   ```

3. **Wait for Service to Start**

   - Admin service takes ~30-45 seconds to fully start
   - Wait 1-2 minutes after starting Docker before accessing

4. **Verify Service Health**

   ```powershell
   # Check if admin container is healthy
   docker ps | findstr "admin"

   # Should show status like "Up 2 minutes (health: starting)" then "Up 2 minutes (healthy)"
   ```

5. **Check Service Logs**

   ```powershell
   docker logs swap-admin-1 | Select-Object -Last 30
   ```

   **Expected output**:

   ```
   [2025-11-24 00:58:04 +0000] [9] [INFO] Starting gunicorn 21.2.0
   [2025-11-24 00:58:04 +0000] [9] [INFO] Listening at: http://0.0.0.0:8005 (9)
   ```

6. **Test Connection**

   ```powershell
   Invoke-WebRequest -Uri "http://localhost:8005/admin/" -UseBasicParsing | Select-Object -ExpandProperty StatusCode

   # Should return: 200
   ```

---

### Issue 2: "Connection Refused" Error

**Problem**: Connection actively refused on port 8005

**Solution**:

```powershell
# Check if port 8005 is in use
netstat -ano | findstr "8005"

# If something else is using it, kill the process or change port in docker-compose.yml
# Or restart all services
docker compose down
docker compose up -d
```

---

### Issue 3: "Invalid Username/Password" After Connection

**Problem**: Credentials don't work after successfully connecting

**Solution**:

1. **Create New Admin User**

   ```powershell
   docker exec swap-admin-1 python manage.py createsuperuser \
     --username admin \
     --email admin@swap.local \
     --noinput
   ```

2. **Set Password**

   ```powershell
   docker exec swap-admin-1 python manage.py shell -c "
   from django.contrib.auth.models import User
   u = User.objects.get(username='admin')
   u.set_password('AdminSwap123!')
   u.save()
   print('Password reset successfully')
   "
   ```

3. **Try Logging In Again**
   - URL: http://localhost:8005/admin/
   - Username: `admin`
   - Password: `AdminSwap123!`

---

### Issue 4: Database Connection Error on Admin

**Problem**: Admin dashboard shows database connection error

**Likely Cause**: PostgreSQL service not running

**Solution**:

```powershell
# Check if postgres is running
docker ps | findstr "postgres"

# Start all services including postgres
docker compose up -d

# Verify postgres is healthy
docker ps | findstr "postgres"
# Should show: "Up X minutes (healthy)"
```

---

### Issue 5: "502 Bad Gateway" or "503 Service Unavailable"

**Problem**: Django admin shows 502/503 error

**Solution**:

```powershell
# Check admin service logs for errors
docker logs swap-admin-1 | Select-Object -Last 50

# Restart admin service
docker restart swap-admin-1

# Wait 30 seconds for service to restart
Start-Sleep -Seconds 30

# Try accessing again
```

---

## Complete Restart Procedure

If all else fails, do a complete reset:

```powershell
cd "c:\Users\Trendig Biz&Tech\Desktop\projects\swap"

# Stop all containers
docker compose down

# Remove volumes (WARNING: This deletes all data)
docker compose down -v

# Rebuild admin image
docker compose build admin

# Start fresh
docker compose up -d

# Wait for services to start (2-3 minutes)
Start-Sleep -Seconds 180

# Verify admin is healthy
docker ps | findstr "admin"

# Create superuser
docker exec swap-admin-1 python manage.py createsuperuser \
  --username admin \
  --email admin@swap.local \
  --noinput

# Set password
docker exec swap-admin-1 python manage.py shell -c "
from django.contrib.auth.models import User
u = User.objects.get(username='admin')
u.set_password('AdminSwap123!')
u.save()
"

# Test access
Invoke-WebRequest -Uri "http://localhost:8005/admin/" -UseBasicParsing | Select-Object -ExpandProperty StatusCode
```

---

## Admin Dashboard Features

Once logged in, you can manage:

### 1. **System Monitor**

- View overall system health
- Check key metrics (users, listings, offers, transactions)
- Monitor escrow balance

### 2. **Disputes**

- Track user disputes
- Update dispute status (open → in_review → resolved → closed)
- Assign priority levels
- View dispute history

### 3. **User Moderation**

- View moderation actions
- Warn users
- Suspend/ban accounts
- Restore or unban users
- Set temporary bans with expiration

### 4. **Audit Logs**

- Complete audit trail of all admin actions
- View before/after changes
- Track IP addresses
- Monitor admin activity for compliance

### 5. **Service Health Checks**

- Monitor all 7 microservices
- Check response times
- Track consecutive failures
- Monitor infrastructure (Kafka, PostgreSQL, Redis)

### 6. **Report Generation**

- Generate daily summaries
- Create weekly analytics
- Export monthly reports
- View dispute reports
- Financial reports
- User activity reports

---

## Credentials Reference

**Default Admin Account** (Created automatically):

- Username: `admin`
- Password: `AdminSwap123!`
- Email: `admin@swap.local`

⚠️ **IMPORTANT**: Change this password in production!

---

## Port Reference

| Service              | Port      | Status |
| -------------------- | --------- | ------ |
| Admin Dashboard      | 8005      | ✅     |
| Auth Service         | 8000      | ✅     |
| User Service         | 8001      | ✅     |
| Listing Service      | 8002      | ✅     |
| Offer Service        | 8003      | ⚠️     |
| Payment Service      | 8004      | ⚠️     |
| Chat Service         | 8006      | ⚠️     |
| Notification Service | 8007      | ⚠️     |
| PostgreSQL           | 5432      | ✅     |
| Redis                | 6379      | ✅     |
| Kafka                | 9092      | ✅     |
| Zookeeper            | 2181      | ✅     |
| MinIO                | 9000-9001 | ✅     |
| Mailhog              | 8025      | ✅     |

---

## Next Steps

1. ✅ Access admin dashboard at http://localhost:8005/admin/
2. ✅ Log in with admin/AdminSwap123!
3. ⏭️ Explore System Monitor to check service health
4. ⏭️ Navigate through Disputes, Moderation, and Audit Logs
5. ⏭️ Generate reports as needed

---

## Support Commands

```powershell
# View admin service logs (last 50 lines)
docker logs swap-admin-1 | Select-Object -Last 50

# Check admin service status
docker inspect swap-admin-1 | Select-Object -ExpandProperty State

# Restart admin service
docker restart swap-admin-1

# Connect to admin container shell
docker exec -it swap-admin-1 bash

# Run Django management commands
docker exec swap-admin-1 python manage.py [command]

# Access Django shell
docker exec -it swap-admin-1 python manage.py shell
```

---

## Troubleshooting Checklist

- [ ] Docker Desktop is running
- [ ] `docker ps` shows 14+ containers
- [ ] `swap-admin-1` container is running and healthy
- [ ] Port 8005 is not blocked by firewall
- [ ] Browser can reach http://localhost:8005/admin/
- [ ] Login credentials are correct (admin / AdminSwap123!)
- [ ] PostgreSQL container is running and healthy
- [ ] No errors in Docker logs: `docker logs swap-admin-1`

---

## FAQ

**Q: Why does the admin dashboard take time to load?**
A: Django migrations run on startup. First load after a restart takes 30-45 seconds.

**Q: Can I change the admin password?**
A: Yes, use Django admin interface or:

```powershell
docker exec -it swap-admin-1 python manage.py changepassword admin
```

**Q: How do I backup admin data?**
A: PostgreSQL admin database is in the `swap_postgres_data` volume. Use standard PostgreSQL backups.

**Q: What if I forgot the admin password?**
A: Use the reset command from Issue 3 above to set it to `AdminSwap123!`

**Q: Can multiple admins be created?**
A: Yes, use `python manage.py createsuperuser` with different usernames.

---

**Last Updated**: November 24, 2025
**Status**: ✅ Admin Dashboard Running
