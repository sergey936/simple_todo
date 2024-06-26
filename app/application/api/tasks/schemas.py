from datetime import datetime

from pydantic import BaseModel

from application.api.schemas import BaseQueryResponseSchema
from domain.entities.tasks import Task


class TaskDetailSchema(BaseModel):
    oid: str
    title: str
    task_body: str
    importance: int
    created_at: datetime
    is_completed: bool = False

    @classmethod
    def from_entity(cls, task: Task) -> 'TaskDetailSchema':
        return cls(
            oid=task.oid,
            title=task.title.as_generic_type(),
            task_body=task.task_body.as_generic_type(),
            importance=task.importance.as_generic_type(),
            is_completed=task.is_completed,
            created_at=task.created_at
        )


class TaskCreateSchema(BaseModel):
    title: str
    task_body: str
    importance: int = 1


class GetTasksQueryResponseSchema(BaseQueryResponseSchema[list[TaskDetailSchema]]):
    ...


class DeleteTaskSchema(BaseModel):
    response: str = 'Task deleted'


class CompleteTaskSchema(BaseModel):
    response: str = 'Task completed'


