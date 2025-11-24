"""
URL Configuration for Swap Admin Service.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from dashboard.views import (
    dashboard_overview,
    service_health,
    recent_disputes,
    audit_log_endpoint,
    dashboard_page,
    HealthCheckView,
)

# Admin site customization
admin.site.site_header = 'Swap Platform Administration'
admin.site.site_title = 'Swap Admin'
admin.site.index_title = 'Welcome to Swap Administration'

router = DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Custom dashboard endpoints
    path('dashboard/', dashboard_page, name='dashboard'),
    path('api/dashboard-overview/', dashboard_overview, name='dashboard_overview'),
    path('api/service-health/', service_health, name='service_health'),
    path('api/recent-disputes/', recent_disputes, name='recent_disputes'),
    path('api/audit-logs/', audit_log_endpoint, name='audit_logs'),
    
    # Standard endpoints
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('health/', HealthCheckView.as_view()),
]
