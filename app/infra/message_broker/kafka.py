from dataclasses import dataclass
from typing import AsyncIterator

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from orjson import orjson

from infra.message_broker.base import BaseMessageBroker


@dataclass
class KafkaMessageBroker(BaseMessageBroker):
    producer: AIOKafkaProducer
    consumer: AIOKafkaConsumer

    async def send_message(self, key: bytes, topic: str, value: bytes):
        await self.producer.send(topic=topic, key=key, value=value)

    async def start_consuming(self, topic: str) -> AsyncIterator[dict]:
        self.consumer.subscribe(topics=[topic])

        async for message in self.consumer:
            yield orjson.loads(message.value)

    async def stop_consuming(self):
        self.consumer.unsubscribe()

    async def stop(self):
        await self.producer.stop()
        await self.consumer.stop()

    async def start(self):
        await self.producer.start()
        await self.consumer.start()
