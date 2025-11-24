"""
Django Admin interface customization for Swap platform.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone

from .models import (
    SystemMonitor,
    Dispute,
    UserModeration,
    AuditLog,
    ServiceHealthCheck,
    ReportGeneration,
)


@admin.register(SystemMonitor)
class SystemMonitorAdmin(admin.ModelAdmin):
    """Admin interface for system monitoring"""
    
    list_display = ['status_badge', 'total_users', 'active_listings', 'pending_offers', 'escrow_balance', 'last_updated']
    readonly_fields = ['last_updated', 'total_users', 'active_listings', 'pending_offers', 'total_transactions', 'escrow_balance']
    
    fieldsets = (
        ('System Status', {
            'fields': ('status',)
        }),
        ('Key Metrics', {
            'fields': ('total_users', 'active_listings', 'pending_offers', 'total_transactions', 'escrow_balance')
        }),
        ('Last Updated', {
            'fields': ('last_updated',),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        colors = {'healthy': '#28a745', 'warning': '#ffc107', 'critical': '#dc3545'}
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Dispute)
class DisputeAdmin(admin.ModelAdmin):
    """Admin interface for dispute management"""
    
    list_display = ['dispute_id', 'status_badge', 'priority_badge', 'reason', 'amount_in_dispute', 'created_at']
    list_filter = ['status', 'priority', 'created_at']
    search_fields = ['dispute_id', 'complainant_id', 'respondent_id', 'reason']
    readonly_fields = ['dispute_id', 'created_at', 'updated_at', 'resolved_at']
    
    fieldsets = (
        ('Dispute Information', {
            'fields': ('dispute_id', 'offer_id', 'reason', 'description')
        }),
        ('Parties', {
            'fields': ('complainant_id', 'respondent_id')
        }),
        ('Status', {
            'fields': ('status', 'priority', 'amount_in_dispute')
        }),
        ('Resolution', {
            'fields': ('resolution', 'resolved_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'resolved_at'),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        colors = {'open': '#17a2b8', 'in_review': '#ffc107', 'resolved': '#28a745', 'closed': '#6c757d'}
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def priority_badge(self, obj):
        colors = {'low': '#28a745', 'medium': '#ffc107', 'high': '#fd7e14', 'critical': '#dc3545'}
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px;">{}</span>',
            colors.get(obj.priority, '#6c757d'),
            obj.get_priority_display()
        )
    priority_badge.short_description = 'Priority'
    
    actions = ['mark_in_review', 'mark_resolved']
    
    def mark_in_review(self, request, queryset):
        updated = queryset.update(status='in_review')
        self.message_user(request, f'{updated} disputes marked as in review.')
    mark_in_review.short_description = 'Mark selected disputes as in review'
    
    def mark_resolved(self, request, queryset):
        updated = queryset.update(status='resolved', resolved_at=timezone.now())
        self.message_user(request, f'{updated} disputes marked as resolved.')
    mark_resolved.short_description = 'Mark selected disputes as resolved'


@admin.register(UserModeration)
class UserModerationAdmin(admin.ModelAdmin):
    """Admin interface for user moderation"""
    
    list_display = ['user_id', 'action_badge', 'severity_badge', 'status_badge', 'created_at', 'expires_at']
    list_filter = ['action', 'severity', 'status_active', 'created_at']
    search_fields = ['user_id', 'reason', 'admin_id']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user_id',)
        }),
        ('Moderation Action', {
            'fields': ('action', 'reason', 'details', 'severity')
        }),
        ('Status', {
            'fields': ('status_active', 'expires_at')
        }),
        ('Admin Information', {
            'fields': ('admin_id',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def action_badge(self, obj):
        colors = {'warning': '#ffc107', 'suspend': '#fd7e14', 'ban': '#dc3545', 'restore': '#28a745', 'unban': '#28a745'}
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px;">{}</span>',
            colors.get(obj.action, '#6c757d'),
            obj.get_action_display()
        )
    action_badge.short_description = 'Action'
    
    def severity_badge(self, obj):
        colors = {1: '#28a745', 2: '#ffc107', 3: '#fd7e14', 4: '#e83e8c', 5: '#dc3545'}
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px;">Level {}</span>',
            colors.get(obj.severity, '#6c757d'),
            obj.severity
        )
    severity_badge.short_description = 'Severity'
    
    def status_badge(self, obj):
        color = '#28a745' if obj.status_active else '#6c757d'
        status_text = 'Active' if obj.status_active else 'Inactive'
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px;">{}</span>',
            color,
            status_text
        )
    status_badge.short_description = 'Status'


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """Admin interface for audit logs"""
    
    list_display = ['admin_id', 'action_badge', 'target_type', 'target_id', 'created_at']
    list_filter = ['action', 'target_type', 'created_at']
    search_fields = ['admin_id', 'target_id', 'reason']
    readonly_fields = ['admin_id', 'action', 'target_type', 'target_id', 'old_values', 'new_values', 'reason', 'ip_address', 'created_at']
    
    fieldsets = (
        ('Action Details', {
            'fields': ('admin_id', 'action', 'reason')
        }),
        ('Target', {
            'fields': ('target_type', 'target_id')
        }),
        ('Changes', {
            'fields': ('old_values', 'new_values')
        }),
        ('Request Information', {
            'fields': ('ip_address', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def action_badge(self, obj):
        colors = {
            'create': '#28a745', 'update': '#17a2b8', 'delete': '#dc3545',
            'suspend': '#fd7e14', 'ban': '#e83e8c', 'restore': '#28a745',
            'resolve_dispute': '#17a2b8', 'release_escrow': '#28a745', 'refund': '#6c757d'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px;">{}</span>',
            colors.get(obj.action, '#6c757d'),
            obj.get_action_display()
        )
    action_badge.short_description = 'Action'
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(ServiceHealthCheck)
class ServiceHealthCheckAdmin(admin.ModelAdmin):
    """Admin interface for service health monitoring"""
    
    list_display = ['service_name_display', 'status_badge', 'response_time_display', 'last_check', 'consecutive_failures']
    list_filter = ['status', 'last_check']
    readonly_fields = ['service_name', 'status', 'response_time_ms', 'last_check', 'error_message', 'consecutive_failures']
    
    fieldsets = (
        ('Service Information', {
            'fields': ('service_name',)
        }),
        ('Health Status', {
            'fields': ('status', 'response_time_ms', 'consecutive_failures')
        }),
        ('Error Information', {
            'fields': ('error_message',)
        }),
        ('Last Check', {
            'fields': ('last_check',)
        }),
    )
    
    def service_name_display(self, obj):
        return obj.get_service_name_display()
    service_name_display.short_description = 'Service'
    
    def status_badge(self, obj):
        colors = {'healthy': '#28a745', 'degraded': '#ffc107', 'down': '#dc3545'}
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def response_time_display(self, obj):
        return f'{obj.response_time_ms}ms'
    response_time_display.short_description = 'Response Time'
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ReportGeneration)
class ReportGenerationAdmin(admin.ModelAdmin):
    """Admin interface for reports"""
    
    list_display = ['title', 'report_type_badge', 'start_date', 'end_date', 'total_volume', 'created_at']
    list_filter = ['report_type', 'created_at']
    search_fields = ['title', 'generated_by']
    readonly_fields = ['created_at', 'summary_data']
    
    fieldsets = (
        ('Report Information', {
            'fields': ('report_type', 'title', 'generated_by')
        }),
        ('Report Period', {
            'fields': ('start_date', 'end_date')
        }),
        ('Summary Data', {
            'fields': ('total_users', 'total_transactions', 'total_volume', 'active_disputes', 'summary_data')
        }),
        ('Created', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def report_type_badge(self, obj):
        colors = {
            'daily_summary': '#17a2b8', 'weekly_analytics': '#6f42c1',
            'monthly_report': '#e83e8c', 'dispute_report': '#dc3545',
            'financial_report': '#28a745', 'user_activity': '#ffc107'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px;">{}</span>',
            colors.get(obj.report_type, '#6c757d'),
            obj.get_report_type_display()
        )
    report_type_badge.short_description = 'Report Type'
