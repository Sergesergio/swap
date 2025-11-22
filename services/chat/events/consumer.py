import os
import asyncio
from shared.kafka import KafkaConsumer
import logging

logger = logging.getLogger(__name__)

class ChatEventConsumer:
    def __init__(self):
        self.consumer = KafkaConsumer(
            bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092"),
            group_id="chat-service",
            topics=[]  # Chat service doesn't consume events currently
        )
        self.running = False
    
    async def start(self):
        if not self.consumer.consumer._topics:  # Skip if no topics
            return
        
        await self.consumer.start()
        self.running = True
        asyncio.create_task(self._process_messages())
    
    async def stop(self):
        self.running = False
        if self.consumer.consumer._topics:
            await self.consumer.stop()
    
    async def _process_messages(self):
        """Process messages from Kafka topics"""
        try:
            async for msg in self.consumer:
                logger.debug(f"Received event: {msg.topic}")
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Error processing messages: {e}")
