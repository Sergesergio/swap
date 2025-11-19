from shared.kafka import KafkaProducer
import os
import logging

logger = logging.getLogger(__name__)

class UserEventProducer:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS")
        )
    
    async def start(self):
        await self.producer.start()
    
    async def stop(self):
        await self.producer.stop()
    
    async def user_rating_updated(self, user_id: int, new_rating: float):
        await self.producer.send_message(
            "user.rating_updated",
            {
                "user_id": user_id,
                "rating": new_rating
            }
        )
    
    async def user_verification_status_changed(
        self,
        user_id: int,
        is_verified: bool
    ):
        await self.producer.send_message(
            "user.verification_status_changed",
            {
                "user_id": user_id,
                "is_verified": is_verified
            }
        )