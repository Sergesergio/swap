from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
from typing import List
import asyncio

from .models import (
    Notification,
    NotificationPreference,
    NotificationCreate,
    NotificationResponse,
    NotificationPreferenceUpdate,
    NotificationPreferenceResponse,
    NotificationType,
)
from .repository.database import get_session, init_db
from .repository.notification_repository import (
    NotificationRepository,
    NotificationPreferenceRepository,
)
from .events.producer import NotificationEventProducer
from .events.consumer import NotificationEventConsumer
from shared.exceptions import ResourceNotFound, ValidationError

app = FastAPI(title="Notification Service")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
notification_producer = None
notification_consumer = None
consumer_task = None


@app.on_event("startup")
async def startup_event():
    global notification_producer, notification_consumer, consumer_task
    
    # Initialize database tables
    init_db()
    
    # Start event handlers
    notification_producer = NotificationEventProducer()
    notification_consumer = NotificationEventConsumer()
    
    await notification_producer.start()
    await notification_consumer.start()
    
    # Start consuming events in background
    consumer_task = asyncio.create_task(
        notification_consumer.consume(handle_event)
    )


@app.on_event("shutdown")
async def shutdown_event():
    global consumer_task
    
    if notification_producer:
        await notification_producer.stop()
    if notification_consumer:
        await notification_consumer.stop()
    if consumer_task:
        consumer_task.cancel()


async def handle_event(topic: str, data: dict):
    """Handle events from other services"""
    # This would typically trigger notification creation
    # For now, just log it
    pass


# Notification endpoints
@app.post("/notifications", response_model=NotificationResponse)
async def create_notification(
    notification_create: NotificationCreate,
    session: Session = Depends(get_session),
):
    """Create a new notification"""
    repo = NotificationRepository(session)
    notification = repo.create_notification(
        user_id=notification_create.user_id,
        notification_type=notification_create.type,
        title=notification_create.title,
        message=notification_create.message,
        data=notification_create.data,
        channels=notification_create.channels,
    )
    
    # Publish event
    await notification_producer.notification_sent(
        user_id=notification.user_id,
        notification_type=notification.type,
        title=notification.title,
        message=notification.message,
        channels=notification.channels,
    )
    
    return NotificationResponse(**notification.dict())


@app.get("/notifications/user/{user_id}", response_model=List[NotificationResponse])
async def get_user_notifications(
    user_id: int,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    unread_only: bool = Query(False),
    session: Session = Depends(get_session),
):
    """Get notifications for a user"""
    repo = NotificationRepository(session)
    notifications = repo.get_user_notifications(
        user_id=user_id,
        limit=limit,
        offset=offset,
        unread_only=unread_only,
    )
    
    return [NotificationResponse(**n.dict()) for n in notifications]


@app.get("/notifications/{notification_id}", response_model=NotificationResponse)
async def get_notification(
    notification_id: int,
    session: Session = Depends(get_session),
):
    """Get a specific notification"""
    repo = NotificationRepository(session)
    notification = repo.get_notification_by_id(notification_id)
    
    if not notification:
        raise ResourceNotFound(f"Notification {notification_id} not found")
    
    return NotificationResponse(**notification.dict())


@app.post("/notifications/{notification_id}/read")
async def mark_notification_read(
    notification_id: int,
    session: Session = Depends(get_session),
):
    """Mark notification as read"""
    repo = NotificationRepository(session)
    success = repo.mark_as_read(notification_id)
    
    if not success:
        raise ResourceNotFound(f"Notification {notification_id} not found")
    
    return {"message": "Notification marked as read"}


@app.post("/users/{user_id}/notifications/read-all")
async def mark_all_notifications_read(
    user_id: int,
    session: Session = Depends(get_session),
):
    """Mark all user notifications as read"""
    repo = NotificationRepository(session)
    count = repo.mark_all_as_read(user_id)
    
    return {"message": f"Marked {count} notifications as read"}


@app.get("/users/{user_id}/notifications/unread-count")
async def get_unread_count(
    user_id: int,
    session: Session = Depends(get_session),
):
    """Get count of unread notifications for user"""
    repo = NotificationRepository(session)
    count = repo.get_unread_count(user_id)
    
    return {"user_id": user_id, "unread_count": count}


@app.delete("/notifications/{notification_id}")
async def delete_notification(
    notification_id: int,
    session: Session = Depends(get_session),
):
    """Delete a notification"""
    repo = NotificationRepository(session)
    success = repo.delete_notification(notification_id)
    
    if not success:
        raise ResourceNotFound(f"Notification {notification_id} not found")
    
    return {"message": "Notification deleted"}


# Notification Preferences endpoints
@app.get(
    "/preferences/{user_id}",
    response_model=NotificationPreferenceResponse,
)
async def get_notification_preferences(
    user_id: int,
    session: Session = Depends(get_session),
):
    """Get notification preferences for user"""
    repo = NotificationPreferenceRepository(session)
    preference = repo.get_preference(user_id)
    
    if not preference:
        # Create default preferences
        preference = repo.create_preference(user_id)
    
    return NotificationPreferenceResponse(**preference.dict())


@app.put(
    "/preferences/{user_id}",
    response_model=NotificationPreferenceResponse,
)
async def update_notification_preferences(
    user_id: int,
    preference_update: NotificationPreferenceUpdate,
    session: Session = Depends(get_session),
):
    """Update notification preferences for user"""
    repo = NotificationPreferenceRepository(session)
    
    # Convert update to dict, removing None values
    update_data = preference_update.dict(exclude_unset=True)
    
    preference = repo.update_preference(user_id, **update_data)
    
    return NotificationPreferenceResponse(**preference.dict())


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "notification",
        "version": "1.0.0",
    }
