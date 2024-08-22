from dataclasses import dataclass
from typing import ClassVar

from domain.events.base import BaseEvent
from domain.values.tasks import Title, Importance, TimeToComplete


@dataclass(frozen=True)
class NewTaskCreatedEvent(BaseEvent):
    event_title: ClassVar[str] = "New task created"

    task_oid: str
    title: str
    importance: str
    time_to_complete: str
    user_oid: str


@dataclass(frozen=True)
class TaskCompletedEvent(BaseEvent):
    event_title: ClassVar[str] = "Task completed"

    task_oid: str
    title: Title
    importance: Importance
    user_oid: str


@dataclass(frozen=True)
class TaskEditedEvent(BaseEvent):
    event_title = "Task edited"

    task_oid: str
    title: str
    user_oid: str
