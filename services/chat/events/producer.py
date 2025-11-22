import os
from shared.kafka import KafkaProducer

class ChatEventProducer:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
        )
    
    async def start(self):
        await self.producer.start()
    
    async def stop(self):
        await self.producer.stop()
    
    async def message_sent(self, conversation_id: int, sender_id: int, data: dict):
        """Publish event when message is sent"""
        await self.producer.send_message(
            topic="chat.message_sent",
            value={
                "conversation_id": conversation_id,
                "sender_id": sender_id,
                **data
            }
        )
    
    async def conversation_created(self, user1_id: int, user2_id: int):
        """Publish event when conversation is created"""
        await self.producer.send_message(
            topic="chat.conversation_created",
            value={
                "user1_id": user1_id,
                "user2_id": user2_id
            }
        )
