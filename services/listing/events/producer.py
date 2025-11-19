from shared.kafka import KafkaProducer
import os
import logging

logger = logging.getLogger(__name__)

class ListingEventProducer:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS")
        )
    
    async def start(self):
        await self.producer.start()
    
    async def stop(self):
        await self.producer.stop()
    
    async def listing_created(self, listing_id: int, user_id: int, data: dict):
        await self.producer.send_message(
            "listing.created",
            {
                "listing_id": listing_id,
                "user_id": user_id,
                **data
            }
        )
    
    async def listing_updated(self, listing_id: int, data: dict):
        await self.producer.send_message(
            "listing.updated",
            {
                "listing_id": listing_id,
                **data
            }
        )
    
    async def listing_deleted(self, listing_id: int, user_id: int):
        await self.producer.send_message(
            "listing.deleted",
            {
                "listing_id": listing_id,
                "user_id": user_id
            }
        )