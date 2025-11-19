from shared.kafka import KafkaConsumer
import os
import logging
from services.offer.repository.offer_repository import OfferRepository

logger = logging.getLogger(__name__)

class OfferEventConsumer:
    def __init__(self, offer_repository: OfferRepository):
        self.consumer = None
        self.offer_repository = offer_repository
        self.bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    
    async def start(self):
        try:
            self.consumer = KafkaConsumer(
                bootstrap_servers=self.bootstrap_servers,
                group_id="offer-service",
                topics=[
                    "payment.held",
                    "payment.released"
                ]
            )
            await self.consumer.start()
            await self.consume_events()
        except Exception as e:
            logger.warning(f"Failed to start Kafka consumer: {e}")
            logger.warning("Offer service will continue without event streaming")
    
    async def stop(self):
        if self.consumer:
            await self.consumer.stop()
    
    async def consume_events(self):
        async for event in self.consumer:
            try:
                if event.topic == "payment.held":
                    await self.handle_payment_held(event.value)
                elif event.topic == "payment.released":
                    await self.handle_payment_released(event.value)
            except Exception as e:
                logger.error(f"Error handling event {event.topic}: {str(e)}")
    
    async def handle_payment_held(self, event_data: dict):
        """Handle when payment service confirms funds are held in escrow"""
        offer_id = event_data["offer_id"]
        offer = await self.offer_repository.get_offer(offer_id)
        if offer:
            await self.offer_repository.update_offer_status(
                offer_id, 
                "payment_held"
            )
            logger.info(f"Updated offer {offer_id} status to payment_held")
    
    async def handle_payment_released(self, event_data: dict):
        """Handle when payment service confirms funds are released from escrow"""
        offer_id = event_data["offer_id"]
        offer = await self.offer_repository.get_offer(offer_id)
        if offer:
            await self.offer_repository.update_offer_status(
                offer_id,
                "completed"
            )
            logger.info(f"Updated offer {offer_id} status to completed")