from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
from ..models import Notification, NotificationPreference, NotificationType


class NotificationRepository:
    """Repository for notification operations"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create_notification(
        self,
        user_id: int,
        notification_type: NotificationType,
        title: str,
        message: str,
        data: Optional[str] = None,
        channels: str = "in_app",
    ) -> Notification:
        """Create a new notification"""
        notification = Notification(
            user_id=user_id,
            type=notification_type,
            title=title,
            message=message,
            data=data,
            channels=channels,
        )
        self.session.add(notification)
        self.session.commit()
        self.session.refresh(notification)
        return notification
    
    def get_notification_by_id(self, notification_id: int) -> Optional[Notification]:
        """Get notification by ID"""
        return self.session.exec(
            select(Notification).where(Notification.id == notification_id)
        ).first()
    
    def get_user_notifications(
        self,
        user_id: int,
        limit: int = 50,
        offset: int = 0,
        unread_only: bool = False,
    ) -> List[Notification]:
        """Get notifications for a user"""
        query = select(Notification).where(Notification.user_id == user_id)
        
        if unread_only:
            query = query.where(Notification.is_read == False)
        
        query = query.order_by(Notification.created_at.desc()).offset(offset).limit(limit)
        return self.session.exec(query).all()
    
    def mark_as_read(self, notification_id: int) -> bool:
        """Mark notification as read"""
        notification = self.get_notification_by_id(notification_id)
        if not notification:
            return False
        
        notification.is_read = True
        notification.read_at = datetime.utcnow()
        notification.updated_at = datetime.utcnow()
        self.session.add(notification)
        self.session.commit()
        return True
    
    def mark_all_as_read(self, user_id: int) -> int:
        """Mark all user notifications as read"""
        notifications = self.session.exec(
            select(Notification).where(
                (Notification.user_id == user_id) & (Notification.is_read == False)
            )
        ).all()
        
        count = 0
        for notification in notifications:
            notification.is_read = True
            notification.read_at = datetime.utcnow()
            notification.updated_at = datetime.utcnow()
            self.session.add(notification)
            count += 1
        
        self.session.commit()
        return count
    
    def get_unread_count(self, user_id: int) -> int:
        """Get count of unread notifications for user"""
        return self.session.exec(
            select(Notification).where(
                (Notification.user_id == user_id) & (Notification.is_read == False)
            )
        ).all().__len__()
    
    def delete_notification(self, notification_id: int) -> bool:
        """Delete a notification"""
        notification = self.get_notification_by_id(notification_id)
        if not notification:
            return False
        
        self.session.delete(notification)
        self.session.commit()
        return True


class NotificationPreferenceRepository:
    """Repository for notification preferences"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def get_preference(self, user_id: int) -> Optional[NotificationPreference]:
        """Get notification preferences for user"""
        return self.session.exec(
            select(NotificationPreference).where(NotificationPreference.user_id == user_id)
        ).first()
    
    def create_preference(self, user_id: int) -> NotificationPreference:
        """Create default notification preferences for user"""
        preference = NotificationPreference(user_id=user_id)
        self.session.add(preference)
        self.session.commit()
        self.session.refresh(preference)
        return preference
    
    def update_preference(
        self,
        user_id: int,
        **kwargs
    ) -> Optional[NotificationPreference]:
        """Update notification preferences"""
        preference = self.get_preference(user_id)
        if not preference:
            preference = self.create_preference(user_id)
        
        for key, value in kwargs.items():
            if value is not None and hasattr(preference, key):
                setattr(preference, key, value)
        
        preference.updated_at = datetime.utcnow()
        self.session.add(preference)
        self.session.commit()
        self.session.refresh(preference)
        return preference
