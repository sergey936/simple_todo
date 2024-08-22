from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable

from application.api.tasks.filters import GetTasksFilters
from domain.entities.tasks import Task
from domain.values.tasks import Title, TaskBody, TimeToComplete


@dataclass
class BaseTaskRepository(ABC):
    @abstractmethod
    async def create_task(self, task: Task) -> None:
        ...

    @abstractmethod
    async def get_tasks_by_user_oid(self, user_oid: str, filters: GetTasksFilters) -> Iterable[Task] | None:
        ...

    @abstractmethod
    async def get_task_by_oid(self, task_oid: str) -> Task | None:
        ...

    @abstractmethod
    async def delete_task(self, task_oid: str) -> None:
        ...

    @abstractmethod
    async def complete_user_task(self, task_oid: str, user_oid: str) -> None:
        ...

    @abstractmethod
    async def edit_task(
            self,
            task_oid: str,
            user_oid: str,
            title: Title,
            task_body: TaskBody,
            time_to_complete: TimeToComplete,
    ):
        ...
