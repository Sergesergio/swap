from aiokafka import AIOKafkaProducer
import json
import os
from datetime import datetime


class NotificationEventProducer:
    """Produces notification events to Kafka"""
    
    def __init__(self):
        self.bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
        self.producer = None
    
    async def start(self):
        """Start Kafka producer"""
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        )
        await self.producer.start()
    
    async def stop(self):
        """Stop Kafka producer"""
        if self.producer:
            await self.producer.stop()
    
    async def notification_sent(
        self,
        user_id: int,
        notification_type: str,
        title: str,
        message: str,
        channels: str = "in_app",
    ):
        """Publish notification sent event"""
        event = {
            "user_id": user_id,
            "type": notification_type,
            "title": title,
            "message": message,
            "channels": channels,
            "timestamp": datetime.utcnow().isoformat(),
        }
        await self.producer.send_and_wait("notification.sent", event)
