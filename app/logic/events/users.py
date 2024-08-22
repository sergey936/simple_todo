from dataclasses import dataclass


from domain.events.users import NewUserCreatedEvent
from infra.message_broker.converters import convert_event_to_broker_message
from logic.events.base import BaseEventHandler


@dataclass
class NewUserCreatedEventHandler(BaseEventHandler[NewUserCreatedEvent, None]):

    async def handle(self, event: NewUserCreatedEvent) -> None:
        await self.message_broker.send_message(
            topic=self.broker_topic,
            value=convert_event_to_broker_message(event=event),
            key=str(event.event_id).encode()
        )
