from dataclasses import dataclass

from domain.entities.base import BaseEntity
from domain.events.tasks import NewTaskCreatedEvent
from domain.values.tasks import Title, TaskBody, Importance


@dataclass
class Task(BaseEntity):
    title: Title
    task_body: TaskBody
    importance: Importance
    user_oid: str

    @classmethod
    def create_task(
            cls,
            title: Title,
            task_body: TaskBody,
            importance: Importance,
            user_oid: str
    ) -> 'Task':

        new_task = Task(
            title=title,
            task_body=task_body,
            importance=importance,
            user_oid=user_oid
        )

        new_task.register_event(
            NewTaskCreatedEvent(
                task_oid=new_task.oid,
                title=title,
                importance=importance,
                user_oid=user_oid
            )
        )

        return new_task
