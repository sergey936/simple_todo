from punq import Container

from infra.message_broker.base import BaseMessageBroker
from logic.init import get_container


async def start():
    container: Container = get_container()
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    await message_broker.start()


async def stop():
    container: Container = get_container()
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    await message_broker.stop()
