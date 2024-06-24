from dataclasses import dataclass
from typing import Iterable

from domain.entities.tasks import Task
from domain.values.tasks import Title, TaskBody, Importance
from infra.repositories.tasks.base import BaseTaskRepository
from infra.repositories.users.base import BaseUserRepository
from logic.commands.base import BaseCommand, BaseCommandHandler
from logic.exceptions.tasks import TaskNotFoundException
from logic.exceptions.users import UserNotFoundException


@dataclass(frozen=True)
class CreateTaskCommand(BaseCommand):
    title: str
    task_body: str
    importance: int
    user_oid: str


@dataclass(frozen=True)
class CreateTaskCommandHandler(BaseCommandHandler):
    task_repository: BaseTaskRepository
    user_repository: BaseUserRepository

    async def handle(self, command: CreateTaskCommand) -> Task:
        user = await self.user_repository.get_user_by_oid(user_oid=command.user_oid)

        if not user:
            raise UserNotFoundException(user_oid=command.user_oid)

        title = Title(command.title)
        task_body = TaskBody(command.task_body)
        importance = Importance(command.importance)

        new_task = Task.create_task(
            title=title,
            task_body=task_body,
            importance=importance,
            user_oid=user.oid
        )

        task = await self.task_repository.create_task(task=new_task)

        return task


@dataclass(frozen=True)
class GetAllUserTasksCommand(BaseCommand):
    user_oid: str


@dataclass(frozen=True)
class GetAllUserTasksCommandHandler(BaseCommandHandler):
    task_repository: BaseTaskRepository
    user_repository: BaseUserRepository

    async def handle(self, command: GetAllUserTasksCommand) -> Iterable[Task]:
        user = await self.user_repository.get_user_by_oid(user_oid=command.user_oid)

        if not user:
            raise UserNotFoundException(user_oid=command.user_oid)

        tasks = await self.task_repository.get_tasks_by_user_oid(user_oid=command.user_oid)

        return tasks


@dataclass(frozen=True)
class DeleteTaskCommand(BaseCommand):
    task_oid: str
    user_oid: str


@dataclass(frozen=True)
class DeleteTaskCommandHandler(BaseCommandHandler):
    task_repository: BaseTaskRepository
    user_repository: BaseUserRepository

    async def handle(self, command: DeleteTaskCommand) -> None:
        user = await self.user_repository.get_user_by_oid(user_oid=command.user_oid)

        if not user:
            raise UserNotFoundException(user_oid=command.user_oid)

        task = await self.task_repository.get_task_by_oid(task_oid=command.task_oid)

        if not task:
            raise TaskNotFoundException(task_oid=command.task_oid)

        if not task.user_oid == command.user_oid:
            raise ...  # TODO Make auth exception (like "you cant do this")

        # TODD register commands in mediator + add sql repo (postgresql)
        await self.task_repository.delete_task(task_oid=command.task_oid)
