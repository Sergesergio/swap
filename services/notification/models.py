from sqlmodel import SQLModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class NotificationType(str, Enum):
    """Types of notifications"""
    OFFER_CREATED = "offer_created"
    OFFER_ACCEPTED = "offer_accepted"
    OFFER_REJECTED = "offer_rejected"
    PAYMENT_HELD = "payment_held"
    PAYMENT_RELEASED = "payment_released"
    MESSAGE_RECEIVED = "message_received"
    LISTING_CREATED = "listing_created"
    LISTING_UPDATED = "listing_updated"
    USER_REGISTERED = "user_registered"
    SYSTEM = "system"


class NotificationChannel(str, Enum):
    """Notification delivery channels"""
    IN_APP = "in_app"
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"


class Notification(SQLModel, table=True):
    """Notification entity"""
    __tablename__ = "notifications"
    
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    type: NotificationType = Field(index=True)
    title: str
    message: str
    data: Optional[str] = None  # JSON string with additional context
    channels: str = Field(default="in_app")  # Comma-separated channels
    is_read: bool = Field(default=False, index=True)
    read_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class NotificationPreference(SQLModel, table=True):
    """User notification preferences"""
    __tablename__ = "notification_preferences"
    
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(unique=True, index=True)
    email_enabled: bool = Field(default=True)
    sms_enabled: bool = Field(default=False)
    push_enabled: bool = Field(default=True)
    in_app_enabled: bool = Field(default=True)
    offer_notifications: bool = Field(default=True)
    payment_notifications: bool = Field(default=True)
    message_notifications: bool = Field(default=True)
    listing_notifications: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# Pydantic models for API requests/responses
class NotificationCreate(SQLModel):
    """Create notification request"""
    user_id: int
    type: NotificationType
    title: str
    message: str
    data: Optional[str] = None
    channels: str = "in_app"


class NotificationResponse(SQLModel):
    """Notification response"""
    id: int
    user_id: int
    type: NotificationType
    title: str
    message: str
    data: Optional[str]
    channels: str
    is_read: bool
    read_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime


class NotificationPreferenceUpdate(SQLModel):
    """Update notification preferences"""
    email_enabled: Optional[bool] = None
    sms_enabled: Optional[bool] = None
    push_enabled: Optional[bool] = None
    in_app_enabled: Optional[bool] = None
    offer_notifications: Optional[bool] = None
    payment_notifications: Optional[bool] = None
    message_notifications: Optional[bool] = None
    listing_notifications: Optional[bool] = None


class NotificationPreferenceResponse(SQLModel):
    """Notification preference response"""
    id: int
    user_id: int
    email_enabled: bool
    sms_enabled: bool
    push_enabled: bool
    in_app_enabled: bool
    offer_notifications: bool
    payment_notifications: bool
    message_notifications: bool
    listing_notifications: bool
    created_at: datetime
    updated_at: datetime
