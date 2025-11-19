from shared.kafka import KafkaProducer
import os
import logging

logger = logging.getLogger(__name__)

class AuthEventProducer:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS")
        )
    
    async def start(self):
        await self.producer.start()
    
    async def stop(self):
        await self.producer.stop()
    
    async def user_registered(self, user_id: int, email: str, username: str):
        await self.producer.send_message(
            "user.created",
            {
                "user_id": user_id,
                "email": email,
                "username": username
            }
        )
    
    async def user_verified_email(self, user_id: int, email: str):
        await self.producer.send_message(
            "user.email_verified",
            {
                "user_id": user_id,
                "email": email
            }
        )