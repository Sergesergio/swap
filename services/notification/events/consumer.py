from aiokafka import AIOKafkaConsumer
import json
import asyncio
import os
from typing import Callable, Optional
import logging

logger = logging.getLogger(__name__)


class NotificationEventConsumer:
    """Consumes events from other services"""
    
    def __init__(self):
        self.bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
        self.consumer = None
        self.running = False
        self.topics = [
            "user.created",
            "listing.created",
            "offer.created",
            "payment.held",
            "payment.released",
            "chat.message.sent",
        ]
    
    async def start(self):
        """Start consuming events"""
        self.consumer = AIOKafkaConsumer(
            *self.topics,
            bootstrap_servers=self.bootstrap_servers,
            group_id="notification-service",
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset="earliest",
        )
        await self.consumer.start()
        self.running = True
        logger.info("Notification consumer started")
    
    async def stop(self):
        """Stop consuming events"""
        self.running = False
        if self.consumer:
            await self.consumer.stop()
        logger.info("Notification consumer stopped")
    
    async def consume(self, callback: Optional[Callable] = None):
        """Consume messages from subscribed topics"""
        try:
            async for message in self.consumer:
                try:
                    logger.info(f"Received event from {message.topic}: {message.value}")
                    if callback:
                        await callback(message.topic, message.value)
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
        except Exception as e:
            logger.error(f"Error consuming messages: {e}")
