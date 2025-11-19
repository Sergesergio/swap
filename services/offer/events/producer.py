from shared.kafka import KafkaProducer
import os
import logging

logger = logging.getLogger(__name__)

class OfferEventProducer:
    def __init__(self):
        self.producer = None
        self.bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    
    async def start(self):
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers
            )
            await self.producer.start()
        except Exception as e:
            logger.warning(f"Failed to start Kafka producer: {e}")
    
    async def stop(self):
        if self.producer:
            await self.producer.stop()
    
    async def offer_created(
        self,
        offer_id: int,
        listing_id: int,
        buyer_id: int,
        seller_id: int,
        offer_type: str
    ):
        if self.producer:
            await self.producer.send_message(
                "offer.created",
                {
                    "offer_id": offer_id,
                    "listing_id": listing_id,
                    "buyer_id": buyer_id,
                    "seller_id": seller_id,
                    "type": offer_type
                }
            )
    
    async def offer_accepted(
        self,
        offer_id: int,
        listing_id: int,
        buyer_id: int,
        seller_id: int,
        price: float = None
    ):
        if self.producer:
            await self.producer.send_message(
                "offer.accepted",
                {
                    "offer_id": offer_id,
                    "listing_id": listing_id,
                    "buyer_id": buyer_id,
                    "seller_id": seller_id,
                    "price": price
                }
            )
    
    async def offer_rejected(
        self,
        offer_id: int,
        listing_id: int,
        buyer_id: int,
        seller_id: int
    ):
        if self.producer:
            await self.producer.send_message(
                "offer.rejected",
                {
                    "offer_id": offer_id,
                    "listing_id": listing_id,
                    "buyer_id": buyer_id,
                    "seller_id": seller_id
                }
            )
    
    async def payment_hold_request(
        self,
        offer_id: int,
        amount: float
    ):
        if self.producer:
            await self.producer.send_message(
                "payment.hold_request",
                {
                    "offer_id": offer_id,
                    "amount": amount
                }
            )