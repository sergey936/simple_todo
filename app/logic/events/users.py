from dataclasses import dataclass

from domain.events.users import NewUserCreatedEvent
from infra.notificators.email import EmailNotificator
from logic.events.base import BaseEventHandler


@dataclass
class NewUserCreatedEventHandler(BaseEventHandler[NewUserCreatedEvent, None]):
    email_notificator: EmailNotificator

    async def handle(self, event: NewUserCreatedEvent) -> None:
        await self.email_notificator.send_notification(
            recipient=event.user_email.as_generic_type(),
            subject='Welcome',
            body=f'{event.username.as_generic_type()}, thank you for registration'
        )
