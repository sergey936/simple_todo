from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable

from domain.entities.tasks import Task


@dataclass
class BaseTaskRepository(ABC):
    @abstractmethod
    async def create_task(self, task: Task):
        ...

    @abstractmethod
    async def get_tasks_by_user_oid(self, user_oid: str) -> Iterable[Task]:
        ...

    @abstractmethod
    async def get_task_by_oid(self, task_oid: str) -> Task:
        ...

    @abstractmethod
    async def delete_task(self, task_oid: str) -> None:
        ...