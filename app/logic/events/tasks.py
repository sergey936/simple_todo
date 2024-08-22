from dataclasses import dataclass

from domain.events.tasks import NewTaskCreatedEvent, TaskCompletedEvent, TaskEditedEvent
from infra.message_broker.converters import convert_event_to_broker_message
from logic.events.base import BaseEventHandler, ET, ER


@dataclass
class NewTaskCreatedEventHandler(BaseEventHandler[NewTaskCreatedEvent, None]):
    async def handle(self, event: NewTaskCreatedEvent) -> None:
        await self.message_broker.send_message(
            topic=self.broker_topic,
            value=convert_event_to_broker_message(event=event),
            key=str(event.event_id).encode()
        )


@dataclass
class TaskCompletedEventHandler(BaseEventHandler[TaskCompletedEvent, None]):
    async def handle(self, event: TaskCompletedEvent) -> None:
        await self.message_broker.send_message(
            topic=self.broker_topic,
            value=convert_event_to_broker_message(event=event),
            key=str(event.event_id).encode()
        )


@dataclass
class TaskEditedEventHandler(BaseEventHandler[TaskEditedEvent, None]):
    async def handle(self, event: TaskEditedEvent) -> None:
        await self.message_broker.send_message(
            topic=self.broker_topic,
            value=convert_event_to_broker_message(event=event),
            key=str(event.event_id).encode()
        )