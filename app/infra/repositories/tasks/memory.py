from dataclasses import dataclass, field
from typing import Iterable

from domain.entities.tasks import Task
from infra.repositories.tasks.base import BaseTaskRepository


@dataclass
class MemoryTaskRepository(BaseTaskRepository):
    _saved_tasks: list[Task] = field(
        default_factory=list,
        kw_only=True
    )

    async def create_task(self, task: Task):
        self._saved_tasks.append(task)

    async def get_tasks_by_user_oid(self, user_oid: str) -> Iterable[Task]:
        tasks = [task for task in self._saved_tasks if task.user_oid == user_oid]

        return tasks

    async def get_task_by_oid(self, task_oid: str) -> Task:
        for task in self._saved_tasks:
            if task.oid == task_oid:
                return task
