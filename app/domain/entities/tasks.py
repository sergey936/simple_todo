from dataclasses import dataclass

from domain.entities.base import BaseEntity
from domain.events.tasks import NewTaskCreatedEvent, TaskCompletedEvent, TaskEditedEvent
from domain.values.tasks import Title, TaskBody, Importance, TimeToComplete


@dataclass
class Task(BaseEntity):
    title: Title
    task_body: TaskBody
    importance: Importance
    time_to_complete: TimeToComplete
    user_oid: str
    is_completed: bool = False

    @classmethod
    def create_task(
            cls,
            title: Title,
            task_body: TaskBody,
            importance: Importance,
            time_to_complete: TimeToComplete,
            user_oid: str
    ) -> 'Task':
        new_task = Task(
            title=title,
            task_body=task_body,
            importance=importance,
            time_to_complete=time_to_complete,
            user_oid=user_oid
        )

        new_task.register_event(
            NewTaskCreatedEvent(
                task_oid=new_task.oid,
                title=title.as_generic_type(),
                importance=importance.as_generic_type(),
                time_to_complete=time_to_complete.as_generic_type(),
                user_oid=user_oid
            )
        )

        return new_task

    def complete_task(self):
        if self.is_completed is False:
            self.is_completed = True
            self.register_event(
                TaskCompletedEvent(
                    task_oid=self.oid,
                    title=self.title.as_generic_type(),
                    importance=self.importance.as_generic_type(),
                    user_oid=self.user_oid
                )
            )

    def update_task(
            self,
            title: Title | None,
            task_body: TaskBody | None,
            time_to_complete: TimeToComplete | None
    ):
        self.title = title or self.title
        self.task_body = task_body or self.task_body
        self.time_to_complete = time_to_complete or self.time_to_complete
        self.register_event(
                TaskEditedEvent(
                    task_oid=self.oid,
                    user_oid=self.user_oid,
                    title=self.title.as_generic_type()
                )
        )
