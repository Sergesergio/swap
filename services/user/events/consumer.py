import os
from shared.kafka import KafkaConsumer
from repository.user_repository import UserRepository
from sqlmodel import Session
from repository.database import get_session
import logging
import asyncio

logger = logging.getLogger(__name__)

class UserEventConsumer:
    def __init__(self):
        self.consumer = KafkaConsumer(
            bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
            group_id="user-service",
            topics=["user.created", "user.verified"]
        )
        self.running = False
    
    async def start(self):
        await self.consumer.start()
        self.running = True
        # Start processing messages in background
        asyncio.create_task(self._process_messages())
    
    async def stop(self):
        self.running = False
        await self.consumer.stop()
    
    async def _process_messages(self):
        """Process messages from Kafka topics"""
        try:
            async for msg in self.consumer:
                if msg.topic == "user.created":
                    await self.handle_user_created(msg.value)
                elif msg.topic == "user.verified":
                    await self.handle_user_verified(msg.value)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Error processing messages: {e}")
    
    async def handle_user_created(self, data: dict):
        try:
            session = next(get_session())
            repository = UserRepository(session)
            
            # Create initial profile
            await repository.create_profile(
                user_id=data["user_id"],
                display_name=data["username"]
            )
            
            # Create wallet
            await repository.create_wallet(user_id=data["user_id"])
            
            logger.info(f"Created profile and wallet for user {data['user_id']}")
        except Exception as e:
            logger.error(f"Error handling user.created event: {e}")
    
    async def handle_user_verified(self, data: dict):
        try:
            session = next(get_session())
            repository = UserRepository(session)
            
            # Update user verification status
            await repository.update_verification_status(
                user_id=data["user_id"],
                is_verified=True
            )
            
            logger.info(f"Updated verification status for user {data['user_id']}")
        except Exception as e:
            logger.error(f"Error handling user.verified event: {e}")