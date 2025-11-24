"""
Admin models for monitoring and managing the Swap platform.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import timedelta


class SystemMonitor(models.Model):
    """Monitor overall system health and metrics"""
    
    STATUS_CHOICES = [
        ('healthy', 'Healthy'),
        ('warning', 'Warning'),
        ('critical', 'Critical'),
    ]
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='healthy')
    total_users = models.IntegerField(default=0)
    active_listings = models.IntegerField(default=0)
    pending_offers = models.IntegerField(default=0)
    total_transactions = models.IntegerField(default=0)
    escrow_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'System Monitor'
        verbose_name_plural = 'System Monitor'
    
    def __str__(self):
        return f'System Status: {self.status}'


class Dispute(models.Model):
    """Track and manage disputes between users"""
    
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_review', 'In Review'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    dispute_id = models.CharField(max_length=50, unique=True, db_index=True)
    offer_id = models.CharField(max_length=50)
    complainant_id = models.CharField(max_length=50)
    respondent_id = models.CharField(max_length=50)
    reason = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    amount_in_dispute = models.DecimalField(max_digits=12, decimal_places=2)
    resolution = models.TextField(blank=True, null=True)
    resolved_by = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['priority', '-created_at']),
        ]
    
    def __str__(self):
        return f'Dispute {self.dispute_id}: {self.reason}'


class UserModeration(models.Model):
    """Track user moderation actions"""
    
    ACTION_CHOICES = [
        ('warning', 'Warning'),
        ('suspend', 'Suspend'),
        ('ban', 'Ban'),
        ('restore', 'Restore'),
        ('unban', 'Unban'),
    ]
    
    user_id = models.CharField(max_length=50, db_index=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    reason = models.CharField(max_length=255)
    details = models.TextField()
    admin_id = models.CharField(max_length=100)
    severity = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    status_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user_id', '-created_at']),
            models.Index(fields=['status_active', 'expires_at']),
        ]
    
    def __str__(self):
        return f'{self.action.title()} for user {self.user_id}'


class AuditLog(models.Model):
    """Track all admin actions for audit purposes"""
    
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('suspend', 'Suspend'),
        ('ban', 'Ban'),
        ('restore', 'Restore'),
        ('resolve_dispute', 'Resolve Dispute'),
        ('release_escrow', 'Release Escrow'),
        ('refund', 'Refund'),
    ]
    
    admin_id = models.CharField(max_length=100, db_index=True)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    target_type = models.CharField(max_length=100)  # e.g., 'User', 'Listing', 'Dispute'
    target_id = models.CharField(max_length=50)
    old_values = models.JSONField(default=dict, blank=True)
    new_values = models.JSONField(default=dict, blank=True)
    reason = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['admin_id', '-created_at']),
            models.Index(fields=['target_type', 'target_id']),
        ]
    
    def __str__(self):
        return f'{self.action} {self.target_type}:{self.target_id} by {self.admin_id}'


class ServiceHealthCheck(models.Model):
    """Monitor health status of individual microservices"""
    
    SERVICE_CHOICES = [
        ('auth', 'Auth Service'),
        ('user', 'User Service'),
        ('listing', 'Listing Service'),
        ('offer', 'Offer Service'),
        ('payment', 'Payment Service'),
        ('chat', 'Chat Service'),
        ('notification', 'Notification Service'),
        ('kafka', 'Kafka'),
        ('postgres', 'PostgreSQL'),
        ('redis', 'Redis'),
    ]
    
    STATUS_CHOICES = [
        ('healthy', 'Healthy'),
        ('degraded', 'Degraded'),
        ('down', 'Down'),
    ]
    
    service_name = models.CharField(max_length=50, choices=SERVICE_CHOICES, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='healthy')
    response_time_ms = models.IntegerField(default=0)
    last_check = models.DateTimeField(auto_now=True)
    error_message = models.TextField(blank=True)
    consecutive_failures = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['service_name']
    
    def __str__(self):
        return f'{self.get_service_name_display()}: {self.status}'


class ReportGeneration(models.Model):
    """Track generated reports and analytics"""
    
    REPORT_TYPE_CHOICES = [
        ('daily_summary', 'Daily Summary'),
        ('weekly_analytics', 'Weekly Analytics'),
        ('monthly_report', 'Monthly Report'),
        ('dispute_report', 'Dispute Report'),
        ('financial_report', 'Financial Report'),
        ('user_activity', 'User Activity'),
    ]
    
    report_type = models.CharField(max_length=50, choices=REPORT_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    generated_by = models.CharField(max_length=100)
    summary_data = models.JSONField(default=dict)
    total_users = models.IntegerField(default=0)
    total_transactions = models.IntegerField(default=0)
    total_volume = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    active_disputes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['report_type', '-created_at']),
        ]
    
    def __str__(self):
        return f'{self.get_report_type_display()}: {self.title}'
