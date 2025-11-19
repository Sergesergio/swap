from typing import Optional, Dict, Any
import json


class KafkaProducer:
    def __init__(self, bootstrap_servers: str):
        # Lazy import to avoid import-time failures if kafka-python/aiokafka
        # versions are incompatible in the image. This pushes the import to
        # runtime when the producer is actually constructed.
        try:
            from aiokafka import AIOKafkaProducer
        except Exception as e:
            raise ImportError(f"aiokafka is required for KafkaProducer: {e}")

        self.producer = AIOKafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    async def start(self):
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()

    async def send_message(
        self,
        topic: str,
        value: Dict[str, Any],
        key: Optional[str] = None
    ):
        try:
            key_bytes = key.encode('utf-8') if key else None
            await self.producer.send_and_wait(topic, value, key=key_bytes)
        except Exception as e:
            # Log error and possibly retry or handle failure
            print(f"Failed to send message to Kafka: {e}")
            raise


class KafkaConsumer:
    def __init__(self, bootstrap_servers: str, group_id: str, topics: list):
        try:
            from aiokafka import AIOKafkaConsumer
        except Exception as e:
            raise ImportError(f"aiokafka is required for KafkaConsumer: {e}")

        self.consumer = AIOKafkaConsumer(
            *topics,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest'
        )

    async def start(self):
        await self.consumer.start()

    async def stop(self):
        await self.consumer.stop()

    async def __aiter__(self):
        """Allow async iteration over messages"""
        async for msg in self.consumer:
            yield msg