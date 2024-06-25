from dataclasses import dataclass
from typing import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from application.api.tasks.filters import GetTasksFilters
from domain.entities.tasks import Task
from infra.db.manager.base import BaseDatabaseManager
from infra.db.models.task import Tasks
from infra.repositories.converters.tasks.converters import convert_task_db_model_to_entity
from infra.repositories.tasks.base import BaseTaskRepository


@dataclass
class PostgresTaskRepository(BaseTaskRepository):
    _database_manager: BaseDatabaseManager

    @property
    async def get_session(self) -> async_sessionmaker:
        return await self._database_manager.get_sessionmaker()

    async def get_task_by_oid(self, task_oid: str) -> Task:
        ...

    async def create_task(self, task: Task) -> None:
        session = await self.get_session

        async with session.begin() as session:
            new_task = Tasks(
                id=task.oid,
                title=task.title.as_generic_type(),
                task_body=task.task_body.as_generic_type(),
                importance=task.importance.as_generic_type(),
                user_id=task.user_oid,
                created_at=task.created_at,
                is_completed=task.is_completed
            )
            session.add(new_task)

            await session.commit()

    async def get_tasks_by_user_oid(self, user_oid: str, filters: GetTasksFilters) -> Iterable[Task] | None:
        session = await self.get_session

        async with session.begin() as session:
            query = select(Tasks).where(Tasks.user_id == user_oid).limit(filters.limit).offset(filters.offset)
            result = await session.execute(query)
            tasks = result.scalars().all()

            if not tasks:
                return None

            return [convert_task_db_model_to_entity(task=task) for task in tasks]

    async def delete_task(self, task_oid: str) -> None:
        ...
