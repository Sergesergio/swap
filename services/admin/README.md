# Swap Admin Service

Django-based administration dashboard for the Swap platform. Provides moderation, dispute resolution, system monitoring, and comprehensive auditing capabilities.

## Features

- **System Monitoring**: Real-time health checks for all microservices (Auth, User, Listing, Offer, Payment, Chat, Notification)
- **Dispute Management**: Track, prioritize, and resolve disputes between users with resolution tracking
- **User Moderation**: Warn, suspend, or ban users with severity levels and expiration dates
- **Audit Logging**: Comprehensive audit trail of all admin actions with old/new values
- **Service Health**: Monitor individual service status, response times, and consecutive failures
- **Report Generation**: Generate daily, weekly, and monthly reports with analytics
- **Django Admin Dashboard**: Full-featured Django superuser interface with custom admin classes

## Architecture

### Database Schema

The Admin service accesses all platform databases in read/write mode:

- `admin`: Primary admin database for moderation and audit data
- `auth`: Authentication service database (read)
- `users`: User profiles and ratings (read)
- `listings`: Active listings (read)
- `offers`: Swap offers and negotiations (read)
- `payments`: Transaction records (read)
- `chat`: Conversations and messages (read)
- `notifications`: User notifications (read)

### Models

#### SystemMonitor

- Tracks overall system health and key metrics
- Monitors total users, active listings, pending offers, transaction count, escrow balance

#### Dispute

- Records disputes between users
- Fields: ID, offer reference, parties, reason, amount, resolution
- Status: open, in_review, resolved, closed
- Priority levels: low, medium, high, critical

#### UserModeration

- Track moderation actions against users
- Action types: warning, suspend, ban, restore, unban
- Severity levels: 1-5
- Optional expiration dates for temporary bans

#### AuditLog

- Complete audit trail of all admin actions
- Captures before/after values (JSONField)
- Tracks: creator, action, target, changes, IP address, timestamp
- Action types: create, update, delete, suspend, ban, resolve_dispute, release_escrow, refund

#### ServiceHealthCheck

- Monitor status of individual microservices
- Tracks: response times, consecutive failures, error messages
- Services: Auth, User, Listing, Offer, Payment, Chat, Notification, Kafka, PostgreSQL, Redis

#### ReportGeneration

- Historical reports and analytics
- Report types: daily_summary, weekly_analytics, monthly_report, dispute_report, financial_report, user_activity
- Stores: summary data (JSON), totals, volume metrics

## Setup

### Installation

```bash
cd services/admin
pip install -r requirements.txt
```

### Configuration

Create `.env` file in the admin service directory:

```env
DEBUG=False
DJANGO_SECRET_KEY=your-secret-key-here
DB_HOST=localhost
DB_PORT=5432
DB_USER=swap_user
DB_PASSWORD=swap_password
ALLOWED_HOSTS=localhost,127.0.0.1,admin.example.com
```

### Database Initialization

```bash
python manage.py migrate
python manage.py createsuperuser
```

Or use the provided init script:

```bash
chmod +x init.sh
./init.sh
```

## Accessing the Dashboard

1. **Web Interface**: http://localhost:8005/admin/

   - Username: `admin`
   - Password: (as created during setup)

2. **Default Credentials** (for development only):
   - Username: `admin`
   - Password: `AdminSwap123!`

## Admin Interface Features

### System Monitor

- View overall system health status (Healthy/Warning/Critical)
- Real-time metrics: users, listings, offers, transactions, escrow balance
- Auto-updated metrics

### Dispute Management

- List all disputes with filtering by status and priority
- Quick status updates with bulk actions (Mark as In Review, Mark as Resolved)
- Detailed dispute view with party information, amounts, and resolution history
- Color-coded status and priority badges

### User Moderation

- View all moderation actions
- Search by user ID or admin
- Filter by action type and severity
- Temporary ban support with expiration dates
- Quick action history for each user

### Audit Logs

- Complete read-only audit trail
- Search by admin ID, target ID, or reason
- Filter by action type and date
- Detailed change tracking (old vs. new values)
- IP address logging

### Service Health

- Monitor status of all platform microservices
- Response time tracking
- Consecutive failure counting
- Error message logging
- Infrastructure services: Kafka, PostgreSQL, Redis

### Reports

- View generated reports and analytics
- Filter by report type and date range
- Access summary data and key metrics
- Historical tracking of platform activity

## API Endpoints

### Health Check

```
GET /health/
```

### Authentication

```
GET /api-auth/login/    # Django session login
GET /api-auth/logout/   # Django session logout
```

## Development

### Django Commands

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Development server
python manage.py runserver 8005

# Create admin data
python manage.py shell < fixtures/seed_admin.py
```

### Testing

```bash
python manage.py test dashboard
```

## Monitoring

### Service Health Checks

The Admin service regularly checks the health of all microservices:

```python
ServiceHealthCheck.objects.filter(status='down')  # Find down services
```

### Audit Trail

Query audit logs for specific actions:

```python
AuditLog.objects.filter(action='ban', admin_id='admin1')
```

### Dispute Analytics

```python
# Open disputes
Dispute.objects.filter(status='open')

# Critical disputes
Dispute.objects.filter(priority='critical').count()

# Disputes by reason
Dispute.objects.values('reason').annotate(count=Count('id'))
```

## Security Considerations

1. **Authentication**: Django session-based with superuser requirement
2. **Authorization**: Admin permission checks on all moderation actions
3. **Audit Trail**: All actions logged with admin ID and IP address
4. **Database Access**: Separate databases with service-specific permissions
5. **HTTPS**: Should be enabled in production
6. **CSRF Protection**: Django CSRF middleware enabled
7. **Secrets**: Django SECRET_KEY must be set to secure random value in production

## Deployment

### Docker Deployment

The Admin service is included in docker-compose.yml:

```bash
docker compose up -d admin
```

Access at: http://localhost:8005/admin/

### Production Deployment

1. Set `DEBUG=False` in environment
2. Configure secure `DJANGO_SECRET_KEY`
3. Update `ALLOWED_HOSTS` with production domain
4. Use secure database credentials
5. Enable HTTPS/SSL
6. Configure proper static file serving (Nginx reverse proxy)
7. Set up regular database backups

## API Documentation

Auto-generated API docs available at:

- Browsable API: `/api/`
- API Authentication: `/api-auth/`

## Troubleshooting

### Database Connection Issues

```bash
# Check PostgreSQL connectivity
python manage.py dbshell
```

### Migration Issues

```bash
# Reset migrations (development only!)
python manage.py migrate dashboard zero
python manage.py migrate dashboard
```

### Static Files Issues

```bash
# Recollect static files
python manage.py collectstatic --clear --noinput
```

## Performance

- Uses PostgreSQL connection pooling
- Implements query optimization with select_related/prefetch_related
- Pagination for list views (50 items per page)
- Database indexes on frequently filtered fields
- Async task support (via Celery, future enhancement)

## Future Enhancements

- [ ] Real-time dashboard with WebSocket updates
- [ ] Advanced analytics and reporting
- [ ] Automated moderation rules engine
- [ ] Integration with payment processing for refunds
- [ ] Bulk import/export for disputes and moderation
- [ ] Custom report builder
- [ ] Email notifications for critical events
- [ ] Two-factor authentication for admins
- [ ] Role-based access control (RBAC)
- [ ] API rate limiting management

## Support

For issues or questions, contact the development team or open an issue in the main repository.
