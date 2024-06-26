from dataclasses import dataclass
from typing import Iterable

from domain.entities.tasks import Task
from infra.repositories.filters.tasks import GetTasksFilters
from infra.repositories.tasks.base import BaseTaskRepository
from infra.repositories.users.base import BaseUserRepository
from logic.exceptions.tasks import GetTasksAccessDenied, UsersTasksNotFoundException, UserTaskNotFound
from logic.exceptions.users import UserNotFoundByIdException
from logic.queries.base import BaseQuery, BaseQueryHandler


@dataclass(frozen=True)
class GetAllUserTasksQuery(BaseQuery):
    user_oid: str
    filters: GetTasksFilters


@dataclass(frozen=True)
class GetAllUserTasksQueryHandler(BaseQueryHandler):
    task_repository: BaseTaskRepository
    user_repository: BaseUserRepository

    async def handle(self, query: GetAllUserTasksQuery) -> Iterable[Task]:
        user = await self.user_repository.get_user_by_oid(user_oid=query.user_oid)

        if not user:
            raise UserNotFoundByIdException(user_oid=query.user_oid)

        tasks = await self.task_repository.get_tasks_by_user_oid(
            user_oid=user.oid,
            filters=query.filters
        )
        if not tasks:
            raise UsersTasksNotFoundException()
        count = len(tasks)

        return tasks, count


@dataclass(frozen=True)
class GetUserTaskByOidQuery(BaseQuery):
    task_oid: str
    user_oid: str


@dataclass(frozen=True)
class GetUserTaskByOidQueryHandler(BaseQueryHandler):
    task_repository: BaseTaskRepository
    user_repository: BaseUserRepository

    async def handle(self, query: GetUserTaskByOidQuery) -> Task:

        user = await self.user_repository.get_user_by_oid(user_oid=query.user_oid)

        if not user:
            raise UserNotFoundByIdException(user_oid=query.user_oid)

        task = await self.task_repository.get_task_by_oid(task_oid=query.task_oid)

        if not task:
            raise UserTaskNotFound(task_oid=query.task_oid)

        return task

