from shared.kafka import KafkaConsumer
import os
import logging
from services.payment.repository.payment_repository import PaymentRepository

logger = logging.getLogger(__name__)

class PaymentEventConsumer:
    def __init__(self, payment_repository: PaymentRepository):
        self.consumer = None
        self.payment_repository = payment_repository
        self.bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
        self.group_id = "payment-service"

    async def start(self):
        try:
            self.consumer = KafkaConsumer(
                bootstrap_servers=self.bootstrap_servers,
                group_id=self.group_id,
                topics=["payment.hold_request"]
            )
            await self.consumer.start()
            await self.consume_events()
        except Exception as e:
            logger.warning(f"Failed to start Kafka consumer: {e}")
            logger.warning("Payment service will continue without event streaming")

    async def stop(self):
        if self.consumer:
            await self.consumer.stop()

    async def consume_events(self):
        async for event in self.consumer:
            try:
                if event.topic == "payment.hold_request":
                    await self.handle_hold_request(event.value)
            except Exception as e:
                logger.error(f"Error handling event {event.topic}: {str(e)}")

    async def handle_hold_request(self, event_data: dict):
        """Handle payment hold request from offer service"""
        offer_id = event_data["offer_id"]
        amount = event_data["amount"]
        
        # Hold the payment
        payment = await self.payment_repository.hold_payment(offer_id, amount)
        logger.info(f"Held payment {payment.id} for offer {offer_id}")
