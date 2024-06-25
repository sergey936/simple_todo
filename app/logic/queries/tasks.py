from dataclasses import dataclass
from typing import Iterable

from domain.entities.tasks import Task
from infra.repositories.filters.tasks import GetTasksFilters
from infra.repositories.tasks.base import BaseTaskRepository
from infra.repositories.users.base import BaseUserRepository
from logic.exceptions.tasks import GetAllTasksAccessDenied
from logic.exceptions.users import UserNotFoundByIdException
from logic.queries.base import BaseQuery, BaseQueryHandler


@dataclass(frozen=True)
class GetAllUserTasksQuery(BaseQuery):
    user_oid: str
    current_user_oid: str
    filters: GetTasksFilters


@dataclass(frozen=True)
class GetAllUserTasksQueryHandler(BaseQueryHandler):
    task_repository: BaseTaskRepository
    user_repository: BaseUserRepository

    async def handle(self, query: GetAllUserTasksQuery) -> Iterable[Task]:
        if not query.user_oid == query.current_user_oid:
            raise GetAllTasksAccessDenied()

        user = await self.user_repository.get_user_by_oid(user_oid=query.current_user_oid)

        if not user:
            raise UserNotFoundByIdException(user_oid=query.current_user_oid)

        tasks = await self.task_repository.get_tasks_by_user_oid(
            user_oid=query.current_user_oid,
            filters=query.filters
        )
        count = len(tasks)

        return tasks, count
