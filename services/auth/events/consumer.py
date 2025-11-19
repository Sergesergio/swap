import os
from shared.kafka import KafkaConsumer
from repository.user_repository import UserRepository
from sqlmodel import Session
from repository.database import get_session
from utils.auth import create_access_token
import logging

logger = logging.getLogger(__name__)

class AuthEventConsumer:
    def __init__(self):
        self.consumer = None
        self.bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    
    async def start(self):
        try:
            # Defer KafkaConsumer creation until actual start
            self.consumer = KafkaConsumer(
                bootstrap_servers=self.bootstrap_servers,
                group_id="auth-service",
                topics=["user.deleted", "user.blocked"]
            )
            # Register handlers
            self.consumer.add_handler("user.deleted", self.handle_user_deleted)
            self.consumer.add_handler("user.blocked", self.handle_user_blocked)
            await self.consumer.start()
        except Exception as e:
            logger.warning(f"Failed to start Kafka consumer: {e}")
            logger.warning("Auth service will continue without event streaming")
    
    async def stop(self):
        if self.consumer:
            await self.consumer.stop()
    
    async def handle_user_deleted(self, data: dict):
        """When a user is deleted, deactivate their auth account"""
        try:
            session = next(get_session())
            repository = UserRepository(session)
            
            # Deactivate user
            user = await repository.get_by_id(data["user_id"])
            if user:
                user.is_active = False
                await repository.update(user.id, user)
                logger.info(f"Deactivated auth account for user {data['user_id']}")
            else:
                logger.warning(f"User {data['user_id']} not found")
        except Exception as e:
            logger.error(f"Error handling user.deleted event: {e}")
    
    async def handle_user_blocked(self, data: dict):
        """When a user is blocked, invalidate their tokens"""
        try:
            session = next(get_session())
            repository = UserRepository(session)
            
            # Block user
            user = await repository.get_by_id(data["user_id"])
            if user:
                user.is_active = False
                await repository.update(user.id, user)
                logger.info(f"Blocked auth account for user {data['user_id']}")
            else:
                logger.warning(f"User {data['user_id']} not found")
        except Exception as e:
            logger.error(f"Error handling user.blocked event: {e}")