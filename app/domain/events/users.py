from dataclasses import dataclass
from typing import ClassVar

from domain.events.base import BaseEvent
from domain.values.users import Email, Username


@dataclass(frozen=True)
class NewUserCreatedEvent(BaseEvent):
    event_title: ClassVar[str] = 'New user created'

    user_oid: str
    user_email: Email
    username: Username
