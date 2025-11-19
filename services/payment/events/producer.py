from shared.kafka import KafkaProducer
import os

class PaymentEventProducer:
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
            print(f"Warning: Failed to start Kafka producer: {e}")

    async def stop(self):
        if self.producer:
            await self.producer.stop()

    async def payment_held(self, payment_id: int, offer_id: int, amount: float):
        if self.producer:
            await self.producer.send_message("payment.held", {"payment_id": payment_id, "offer_id": offer_id, "amount": amount})

    async def payment_released(self, payment_id: int, offer_id: int, amount: float):
        if self.producer:
            await self.producer.send_message("payment.released", {"payment_id": payment_id, "offer_id": offer_id, "amount": amount})
