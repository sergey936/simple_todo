from dataclasses import dataclass
from typing import ClassVar

from domain.events.base import BaseEvent
from domain.values.tasks import Title, Importance


@dataclass(frozen=True)
class NewTaskCreatedEvent(BaseEvent):
    event_title: ClassVar[str] = "New task created"

    task_oid: str
    title: Title
    importance: Importance

