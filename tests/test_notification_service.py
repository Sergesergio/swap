"""
Comprehensive Notification Service Tests

Tests for notification creation, management, and preferences.
"""

import pytest
from datetime import datetime
import sys
from pathlib import Path

# Add workspace root and services directory to path for imports
root_path = Path(__file__).parent.parent
services_path = root_path / "services"
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))
if str(services_path) not in sys.path:
    sys.path.insert(0, str(services_path))

# Import Notification service components with full module path
from notification.main import app
from notification.models import (
    Notification,
    NotificationPreference,
    NotificationCreate,
    NotificationType,
    NotificationChannel,
    NotificationPreferenceUpdate,
)


@pytest.fixture
def test_users():
    """Fixture providing test user IDs"""
    return {
        "user1": 1,
        "user2": 2,
        "user3": 3,
    }


@pytest.fixture
def test_notification_data(test_users):
    """Fixture providing test notification data"""
    return {
        "user_id": test_users["user1"],
        "type": NotificationType.OFFER_CREATED,
        "title": "New Offer Received",
        "message": "Someone has made an offer on your item",
        "data": '{"offer_id": 123}',
        "channels": NotificationChannel.IN_APP,
    }


class TestNotificationHealthCheck:
    """Test Notification service health endpoint"""

    def test_health_endpoint_exists(self):
        """Verify health endpoint is defined"""
        routes = [route.path for route in app.routes]
        assert "/health" in routes


class TestNotificationTypeEnum:
    """Test NotificationType enum"""

    def test_notification_types_defined(self):
        """Verify all notification types are defined"""
        assert NotificationType.OFFER_CREATED
        assert NotificationType.OFFER_ACCEPTED
        assert NotificationType.OFFER_REJECTED
        assert NotificationType.PAYMENT_HELD
        assert NotificationType.PAYMENT_RELEASED
        assert NotificationType.MESSAGE_RECEIVED
        assert NotificationType.LISTING_CREATED
        assert NotificationType.LISTING_UPDATED
        assert NotificationType.USER_REGISTERED
        assert NotificationType.SYSTEM

    def test_notification_type_values(self):
        """Verify notification type values"""
        assert NotificationType.OFFER_CREATED.value == "offer_created"
        assert NotificationType.PAYMENT_HELD.value == "payment_held"


class TestNotificationChannelEnum:
    """Test NotificationChannel enum"""

    def test_notification_channels_defined(self):
        """Verify notification channels are defined"""
        assert NotificationChannel.IN_APP
        assert NotificationChannel.EMAIL
        assert NotificationChannel.SMS
        assert NotificationChannel.PUSH


class TestNotificationModel:
    """Test Notification model"""

    def test_notification_creation(self, test_notification_data):
        """Verify Notification creation"""
        notification = Notification(
            user_id=test_notification_data["user_id"],
            type=test_notification_data["type"],
            title=test_notification_data["title"],
            message=test_notification_data["message"],
            data=test_notification_data["data"],
            channels=test_notification_data["channels"],
        )
        assert notification.user_id == test_notification_data["user_id"]
        assert notification.type == test_notification_data["type"]
        assert notification.title == test_notification_data["title"]

    def test_notification_read_default_false(self, test_notification_data):
        """Verify notification starts as unread"""
        notification = Notification(
            user_id=test_notification_data["user_id"],
            type=test_notification_data["type"],
            title=test_notification_data["title"],
            message=test_notification_data["message"],
        )
        assert notification.is_read is False

    def test_notification_read_at_default_none(self, test_notification_data):
        """Verify read_at is initially None"""
        notification = Notification(
            user_id=test_notification_data["user_id"],
            type=test_notification_data["type"],
            title=test_notification_data["title"],
            message=test_notification_data["message"],
        )
        assert notification.read_at is None

    def test_notification_has_timestamps(self, test_notification_data):
        """Verify notification has created_at and updated_at"""
        notification = Notification(
            user_id=test_notification_data["user_id"],
            type=test_notification_data["type"],
            title=test_notification_data["title"],
            message=test_notification_data["message"],
        )
        assert hasattr(notification, "created_at")
        assert hasattr(notification, "updated_at")


class TestNotificationCreateModel:
    """Test NotificationCreate model"""

    def test_notification_create_valid(self, test_notification_data):
        """Verify NotificationCreate with valid data"""
        create = NotificationCreate(
            user_id=test_notification_data["user_id"],
            type=test_notification_data["type"],
            title=test_notification_data["title"],
            message=test_notification_data["message"],
        )
        assert create.user_id == test_notification_data["user_id"]

    def test_notification_create_with_channels(self, test_notification_data):
        """Verify NotificationCreate accepts channels"""
        create = NotificationCreate(
            user_id=test_notification_data["user_id"],
            type=test_notification_data["type"],
            title=test_notification_data["title"],
            message=test_notification_data["message"],
            channels="in_app,email",
        )
        assert "in_app" in create.channels
        assert "email" in create.channels


class TestNotificationPreferenceModel:
    """Test NotificationPreference model"""

    def test_preference_creation(self, test_users):
        """Verify NotificationPreference creation"""
        preference = NotificationPreference(user_id=test_users["user1"])
        assert preference.user_id == test_users["user1"]

    def test_preference_defaults(self, test_users):
        """Verify NotificationPreference default values"""
        preference = NotificationPreference(user_id=test_users["user1"])
        assert preference.email_enabled is True
        assert preference.sms_enabled is False
        assert preference.push_enabled is True
        assert preference.in_app_enabled is True
        assert preference.offer_notifications is True
        assert preference.payment_notifications is True
        assert preference.message_notifications is True
        assert preference.listing_notifications is True

    def test_preference_all_fields(self, test_users):
        """Verify NotificationPreference with all fields"""
        now = datetime.utcnow()
        preference = NotificationPreference(
            user_id=test_users["user1"],
            email_enabled=False,
            sms_enabled=True,
            push_enabled=False,
            in_app_enabled=True,
            offer_notifications=False,
            payment_notifications=False,
            message_notifications=True,
            listing_notifications=False,
            created_at=now,
            updated_at=now,
        )
        assert preference.email_enabled is False
        assert preference.sms_enabled is True
        assert preference.push_enabled is False


class TestNotificationPreferenceUpdateModel:
    """Test NotificationPreferenceUpdate model"""

    def test_preference_update_partial(self):
        """Verify NotificationPreferenceUpdate with partial updates"""
        update = NotificationPreferenceUpdate(
            email_enabled=False,
            sms_enabled=True,
        )
        assert update.email_enabled is False
        assert update.sms_enabled is True
        # Other fields should be None
        assert update.push_enabled is None

    def test_preference_update_empty(self):
        """Verify NotificationPreferenceUpdate can be empty"""
        update = NotificationPreferenceUpdate()
        # All fields should be None
        assert update.email_enabled is None
        assert update.sms_enabled is None


class TestAppStructure:
    """Test Notification service app structure"""

    def test_app_exists(self):
        """Verify FastAPI app is created"""
        assert app is not None

    def test_app_title(self):
        """Verify app has correct title"""
        assert app.title == "Notification Service"

    def test_health_route_exists(self):
        """Verify /health route is registered"""
        routes = [route.path for route in app.routes]
        assert "/health" in routes

    def test_notification_routes_exist(self):
        """Verify notification routes are registered"""
        routes = [route.path for route in app.routes]
        has_notification_routes = any("notifications" in route for route in routes)
        assert has_notification_routes

    def test_preference_routes_exist(self):
        """Verify preference routes are registered"""
        routes = [route.path for route in app.routes]
        has_preference_routes = any("preferences" in route for route in routes)
        assert has_preference_routes


class TestNotificationTitleAndMessage:
    """Test notification content handling"""

    def test_notification_with_long_title(self, test_notification_data):
        """Verify notification accepts long title"""
        long_title = "a" * 500
        notification = Notification(
            user_id=test_notification_data["user_id"],
            type=test_notification_data["type"],
            title=long_title,
            message=test_notification_data["message"],
        )
        assert len(notification.title) == 500

    def test_notification_with_long_message(self, test_notification_data):
        """Verify notification accepts long message"""
        long_message = "m" * 5000
        notification = Notification(
            user_id=test_notification_data["user_id"],
            type=test_notification_data["type"],
            title=test_notification_data["title"],
            message=long_message,
        )
        assert len(notification.message) == 5000

    def test_notification_with_unicode(self, test_notification_data):
        """Verify notification handles unicode"""
        unicode_title = "你好 🌍 مرحبا"
        notification = Notification(
            user_id=test_notification_data["user_id"],
            type=test_notification_data["type"],
            title=unicode_title,
            message=test_notification_data["message"],
        )
        assert notification.title == unicode_title


class TestMultipleUsers:
    """Test handling multiple users"""

    def test_notifications_for_different_users(self, test_users, test_notification_data):
        """Verify different users can have notifications"""
        notif1 = Notification(
            user_id=test_users["user1"],
            type=NotificationType.OFFER_CREATED,
            title="Offer 1",
            message="Message 1",
        )
        notif2 = Notification(
            user_id=test_users["user2"],
            type=NotificationType.PAYMENT_HELD,
            title="Offer 2",
            message="Message 2",
        )
        assert notif1.user_id != notif2.user_id
        assert notif1.type != notif2.type


class TestNotificationChannels:
    """Test notification channel handling"""

    def test_notification_single_channel(self, test_notification_data):
        """Verify single channel notification"""
        notification = Notification(
            user_id=test_notification_data["user_id"],
            type=test_notification_data["type"],
            title=test_notification_data["title"],
            message=test_notification_data["message"],
            channels="email",
        )
        assert notification.channels == "email"

    def test_notification_multiple_channels(self, test_notification_data):
        """Verify multiple channels notification"""
        notification = Notification(
            user_id=test_notification_data["user_id"],
            type=test_notification_data["type"],
            title=test_notification_data["title"],
            message=test_notification_data["message"],
            channels="email,sms,push",
        )
        assert "email" in notification.channels
        assert "sms" in notification.channels


# Integration test markers (to be run with Docker)
@pytest.mark.skip(reason="Requires active database and services")
class TestDatabaseIntegration:
    """Database integration tests"""

    def test_create_notification_persists(self):
        """Test notification persists to database"""
        pass

    def test_notification_retrieval(self):
        """Test retrieving notifications from database"""
        pass

    def test_mark_as_read(self):
        """Test marking notification as read"""
        pass


@pytest.mark.skip(reason="Requires Kafka service running")
class TestKafkaIntegration:
    """Integration tests for Kafka event streaming"""

    def test_notification_event_published(self):
        """Test notification.sent event is published"""
        pass

    def test_consume_user_created_event(self):
        """Test consuming user.created events"""
        pass

    def test_consume_offer_created_event(self):
        """Test consuming offer.created events"""
        pass
