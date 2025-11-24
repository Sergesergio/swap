"""
Custom admin views for the Swap dashboard.
Provides REST API endpoints for modern admin interface.
"""

from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from datetime import datetime, timedelta
from django.db.models import Count, Sum
import json

from .models import (
    SystemMonitor,
    Dispute,
    UserModeration,
    AuditLog,
    ServiceHealthCheck,
    ReportGeneration,
)


@login_required
@require_http_methods(["GET"])
def dashboard_overview(request):
    """
    API endpoint returning dashboard overview statistics
    """
    try:
        # Get latest system monitor
        system_monitor = SystemMonitor.objects.first()
        
        # Dispute statistics
        disputes = Dispute.objects.all()
        dispute_stats = {
            'total': disputes.count(),
            'open': disputes.filter(status='open').count(),
            'in_review': disputes.filter(status='in_review').count(),
            'resolved': disputes.filter(status='resolved').count(),
            'closed': disputes.filter(status='closed').count(),
        }
        
        # Moderation statistics
        moderation = UserModeration.objects.all()
        moderation_stats = {
            'total_actions': moderation.count(),
            'warnings': moderation.filter(action_type='warn').count(),
            'suspensions': moderation.filter(action_type='suspend').count(),
            'bans': moderation.filter(action_type='ban').count(),
            'active': moderation.filter(action_type__in=['suspend', 'ban']).filter(
                expiration_date__gte=datetime.now() if moderation.filter(expiration_date__isnull=False).exists() else None
            ).count() if moderation.exists() else 0,
        }
        
        # Service health statistics
        services = ServiceHealthCheck.objects.all()
        service_stats = {
            'total_services': services.count(),
            'healthy': services.filter(status='healthy').count(),
            'warning': services.filter(status='warning').count(),
            'critical': services.filter(status='critical').count(),
            'avg_response_time': services.aggregate(Sum('response_time_ms'))['response_time_ms__sum'] // max(services.count(), 1),
        }
        
        # Audit log statistics
        audit_logs = AuditLog.objects.all()
        last_24h = datetime.now() - timedelta(days=1)
        audit_stats = {
            'total_actions': audit_logs.count(),
            'actions_today': audit_logs.filter(timestamp__gte=last_24h).count(),
        }
        
        return JsonResponse({
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'system_monitor': {
                'status': system_monitor.status if system_monitor else 'unknown',
                'total_users': system_monitor.total_users if system_monitor else 0,
                'active_listings': system_monitor.active_listings if system_monitor else 0,
                'pending_offers': system_monitor.pending_offers if system_monitor else 0,
                'total_transactions': system_monitor.total_transactions if system_monitor else 0,
                'escrow_balance': float(system_monitor.escrow_balance) if system_monitor else 0.0,
            },
            'disputes': dispute_stats,
            'moderation': moderation_stats,
            'services': service_stats,
            'audit': audit_stats,
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e),
        }, status=500)


@login_required
@require_http_methods(["GET"])
def service_health(request):
    """
    API endpoint returning detailed service health information
    """
    try:
        services = ServiceHealthCheck.objects.all().values(
            'service_name', 'status', 'response_time_ms', 'consecutive_failures', 'last_check'
        )
        
        return JsonResponse({
            'status': 'success',
            'services': list(services),
            'timestamp': datetime.now().isoformat(),
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e),
        }, status=500)


@login_required
@require_http_methods(["GET"])
def recent_disputes(request):
    """
    API endpoint returning recent disputes
    """
    try:
        limit = int(request.GET.get('limit', 10))
        disputes = Dispute.objects.all().order_by('-created_at')[:limit]
        
        dispute_data = []
        for dispute in disputes:
            dispute_data.append({
                'id': str(dispute.id),
                'dispute_id': dispute.dispute_id,
                'reason': dispute.reason,
                'status': dispute.status,
                'priority': dispute.priority,
                'amount': float(dispute.amount_in_dispute),
                'created_at': dispute.created_at.isoformat(),
            })
        
        return JsonResponse({
            'status': 'success',
            'disputes': dispute_data,
            'count': len(dispute_data),
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e),
        }, status=500)


@login_required
@require_http_methods(["GET"])
def audit_log_endpoint(request):
    """
    API endpoint returning audit logs
    """
    try:
        limit = int(request.GET.get('limit', 20))
        logs = AuditLog.objects.all().order_by('-timestamp')[:limit]
        
        log_data = []
        for log in logs:
            log_data.append({
                'id': str(log.id),
                'admin': log.admin_user,
                'model': log.model_name,
                'action': log.action_type,
                'timestamp': log.timestamp.isoformat(),
                'ip_address': log.ip_address,
            })
        
        return JsonResponse({
            'status': 'success',
            'logs': log_data,
            'count': len(log_data),
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e),
        }, status=500)


@login_required
@require_http_methods(["GET"])
def dashboard_page(request):
    """
    Render custom dashboard page with modern UI
    """
    context = {
        'title': 'Swap Admin Dashboard',
        'user': request.user,
    }
    return render(request, 'dashboard.html', context)


class HealthCheckView(View):
    """Simple health check endpoint for Docker health monitoring"""
    
    @method_decorator(csrf_exempt)
    def get(self, request):
        return JsonResponse({'status': 'healthy'})
