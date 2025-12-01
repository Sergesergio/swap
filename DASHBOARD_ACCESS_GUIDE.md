# Admin Dashboard Access & Navigation Guide

## 🎯 Where to Go

### Main Entry Points

```
┌─────────────────────────────────────────────────────────────┐
│  SWAP ADMIN DASHBOARD                                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1️⃣  MODERN DASHBOARD (NEW!)                               │
│     → http://localhost:8005/dashboard/                     │
│     → Beautiful real-time monitoring                       │
│     → Recommended for most users                           │
│                                                             │
│  2️⃣  TRADITIONAL ADMIN                                      │
│     → http://localhost:8005/admin/                         │
│     → Django admin with modern theme                       │
│     → For detailed management                              │
│                                                             │
│  3️⃣  API ENDPOINTS (For Developers)                         │
│     → http://localhost:8005/api/dashboard-overview/        │
│     → http://localhost:8005/api/service-health/            │
│     → http://localhost:8005/api/recent-disputes/           │
│     → http://localhost:8005/api/audit-logs/                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 📊 Dashboard Layout

### Main Dashboard (http://localhost:8005/dashboard/)

```
┌─────────────────────────────────────────────────────────────┐
│  📊 Swap Admin Dashboard        [🔄 Refresh Data]          │
│  Real-time platform monitoring and administration           │
└─────────────────────────────────────────────────────────────┘

┌──────────────────────┬──────────────────────┬──────────────┐
│  📈 System Status    │  ⚖️ Disputes         │  👥 Moderation
├──────────────────────┼──────────────────────┼──────────────┤
│  Status: Healthy     │  Total: 5            │  Total: 15
│  Users: 150          │  Open: 2             │  Warnings: 8
│  Listings: 45        │  In Review: 1        │  Suspend: 4
│  Pending Offers: 12  │  Resolved: 1         │  Bans: 3
│  Transactions: 523   │  Closed: 1           │  Active: 7
│  Escrow: $15,000.50  │                      │
└──────────────────────┴──────────────────────┴──────────────┘

┌──────────────────────────────────────────────────────────────┐
│  🔧 Service Health Details                                  │
├──────────────────────────────────────────────────────────────┤
│  Service Name         │ Status  │ Response │ Failures │ Time
├──────────────────────┼─────────┼─────────┼──────────┼──────┤
│  Auth Service        │ ✅ OK   │ 145ms   │ 0        │ Now
│  User Service        │ ✅ OK   │ 152ms   │ 0        │ Now
│  Listing Service     │ ✅ OK   │ 168ms   │ 0        │ Now
│  Offer Service       │ ⚠️  Warn│ 245ms   │ 1        │ 30s
│  Payment Service     │ ⚠️  Warn│ 312ms   │ 2        │ 1m
│  Chat Service        │ ⚠️  Warn│ 189ms   │ 0        │ 45s
│  Notification Svc    │ ✅ OK   │ 176ms   │ 0        │ Now
└──────────────────────┴─────────┴─────────┴──────────┴──────┘

┌──────────────────────────────────────────────────────────────┐
│  ⚡ Recent Disputes                                           │
├──────────────────────────────────────────────────────────────┤
│  ID │ Reason              │ Status   │ Priority │ Amount │ Date
├────┼────────────────────┼──────────┼──────────┼────────┼──────┤
│ 1  │ Product not as desc│ Open     │ High     │ $450   │ Now
│ 2  │ Payment issue      │ Resolved │ Medium   │ $125   │ 1h
│ 3  │ Scam attempt       │ Closed   │ Critical │ $890   │ 2h
└────┴────────────────────┴──────────┴──────────┴────────┴──────┘
```

## 🎨 Color Legend

```
Status Colors:
─────────────────────────────
🟢 Green = Healthy/Good       (Active, resolved, OK)
🟡 Yellow = Warning/Caution   (Degraded, pending, alert)
🔴 Red = Critical/Error       (Failed, banned, problem)
```

## 🔑 Login Screen

```
┌─────────────────────────────────────────────────────────────┐
│                   Swap Platform Administration              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Username: [______________________]                        │
│  Password: [______________________]                        │
│                                                             │
│             [ LOGIN ]    [ FORGOT? ]                        │
│                                                             │
│  Remember me: ☐                                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘

Credentials:
  Username: admin
  Password: AdminSwap123!
```

## 📱 Mobile View

```
┌──────────────────────────┐
│ 📊 Swap Admin            │
│ ☰ Menu                   │
├──────────────────────────┤
│                          │
│ 📈 System               │
│  Status: ✅ Healthy     │
│  Users: 150             │
│  Listings: 45           │
│  Offers: 12             │
│                          │
│ ⚖️ Disputes              │
│  Total: 5               │
│  Open: 2                │
│                          │
│ 👥 Moderation            │
│  Actions: 15            │
│  Bans: 3                │
│                          │
│ 🔧 Service Health        │
│  Healthy: 5/7           │
│  Avg Time: 180ms        │
│                          │
└──────────────────────────┘
```

## 🧭 Navigation Flow

```
                         START HERE
                             ↓
                    http://localhost:8005/
                             ↓
         ┌────────────────────┼────────────────────┐
         ↓                    ↓                    ↓
    /dashboard/           /admin/            /api/*/
    (NEW MODERN)       (TRADITIONAL)      (FOR DEVS)
         ↓                    ↓                    ↓
    ┌─────────┐          ┌─────────┐         ┌─────────┐
    │ Cards & │          │ Models  │         │  JSON   │
    │ Charts  │          │ List    │         │ Data    │
    │ Tables  │          │ Edit    │         │ Streams │
    │ Real-   │          │ Delete  │         │ API     │
    │ time    │          │ Add     │         │ calls   │
    └─────────┘          └─────────┘         └─────────┘
```

## 🎯 What to Do in Each Section

### Modern Dashboard (Recommended)

```
✅ Monitor system health
✅ Check service status
✅ View recent disputes
✅ See moderation stats
✅ Quick overview of platform
❌ Cannot edit directly (view-only)
```

### Traditional Admin

```
✅ Create new records
✅ Edit existing data
✅ Delete records
✅ Perform bulk actions
✅ Detailed management
✅ Advanced filtering
❌ Less visual appeal
```

### API Endpoints

```
✅ Programmatic access
✅ External integrations
✅ Automation
✅ Custom dashboards
✅ Mobile apps
✅ JSON responses
❌ Requires API knowledge
```

## 🔄 Data Refresh

```
Dashboard Auto-Refresh Timeline:
─────────────────────────────────────────────────────────────

Time    │ Action
────────┼─────────────────────────────────────────────────
0:00    │ Load dashboard
0:05    │ Display initial data
0:30    │ 🔄 Auto-refresh #1
1:00    │ 🔄 Auto-refresh #2
1:30    │ 🔄 Auto-refresh #3
...     │ ...
        │ Manual refresh button always available
```

## ⚡ Quick Actions

### From Dashboard

```
[🔄 Refresh Data]     → Manually refresh all metrics
[View Details]        → Click any card for more info
[Drill Down]          → Click service for health details
[Filter Data]         → Search disputes or logs
```

### From Admin

```
[Add New]             → Create new dispute/moderation
[Edit]                → Modify existing records
[Delete]              → Remove record (with confirmation)
[Bulk Actions]        → Perform action on multiple items
[Export]              → Download data as CSV
[Filter]              → Advanced filtering
[Search]              → Full-text search
```

## 💡 Tips & Tricks

### Performance

- Dashboard loads ~1-2 seconds first time
- API responses cached (~5 seconds)
- Auto-refresh every 30 seconds (adjustable)

### Troubleshooting

- If no data shows: Check service health
- If page slow: Clear browser cache (Ctrl+Shift+Delete)
- If styles look wrong: Hard refresh (Ctrl+Shift+R)

### Best Practices

1. Check dashboard first for quick overview
2. Go to admin for detailed management
3. Use API for programmatic access
4. Monitor service health regularly
5. Review disputes and moderation logs daily

## 🔗 Quick Links

```
Main Dashboard:     http://localhost:8005/dashboard/
Admin Interface:    http://localhost:8005/admin/
API Overview:       http://localhost:8005/api/dashboard-overview/
Health Check:       http://localhost:8005/api/service-health/
Recent Disputes:    http://localhost:8005/api/recent-disputes/
Audit Logs:         http://localhost:8005/api/audit-logs/
Health Endpoint:    http://localhost:8005/health/
```

## 📋 Common Workflows

### Monitor System Health

```
1. Open http://localhost:8005/dashboard/
2. Check 📈 System Status card
3. Review 🔧 Service Health Details
4. If warning/critical → Go to admin for details
```

### Manage a Dispute

```
1. Go to http://localhost:8005/admin/
2. Click "Disputes"
3. Find the dispute
4. Update status (open → in_review → resolved → closed)
5. Save changes
```

### Check User Moderation

```
1. Go to http://localhost:8005/dashboard/
2. Check 👥 User Moderation card
3. For details → Go to http://localhost:8005/admin/
4. Find user moderation action
5. View or update
```

### Monitor Service Status

```
1. Open dashboard: http://localhost:8005/dashboard/
2. Scroll to 🔧 Service Health Details
3. Red/Yellow = Issues, Green = OK
4. Click service name for details
5. Check response times and failures
```

---

**Status**: ✅ Complete  
**Theme**: 🎨 Modern Dark  
**Access**: 🌐 http://localhost:8005  
**Update**: ⏱️ Last refreshed now
