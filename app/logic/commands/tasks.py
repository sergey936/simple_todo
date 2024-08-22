import datetime
from dataclasses import dataclass

from domain.entities.tasks import Task
from domain.values.tasks import Title, TaskBody, Importance, TimeToComplete
from infra.repositories.tasks.base import BaseTaskRepository
from infra.repositories.users.base import BaseUserRepository
from logic.commands.base import BaseCommand, BaseCommandHandler, CT, CR
from logic.exceptions.tasks import TaskNotFoundException, TaskAccessDeniedException, GetTasksAccessDenied
from logic.exceptions.users import UserNotFoundByIdException


@dataclass(frozen=True)
class CreateTaskCommand(BaseCommand):
    title: str
    task_body: str
    importance: int
    user_oid: str
    time_limit: datetime.date


@dataclass(frozen=True)
class CreateTaskCommandHandler(BaseCommandHandler):
    task_repository: BaseTaskRepository
    user_repository: BaseUserRepository

    async def handle(self, command: CreateTaskCommand) -> Task:
        user = await self.user_repository.get_user_by_oid(user_oid=command.user_oid)

        if not user:
            raise UserNotFoundByIdException(user_oid=command.user_oid)

        title = Title(command.title)
        task_body = TaskBody(command.task_body)
        importance = Importance(command.importance)
        time_to_complete = TimeToComplete((command.time_limit - datetime.date.today()).total_seconds())

        new_task = Task.create_task(
            title=title,
            task_body=task_body,
            importance=importance,
            time_to_complete=time_to_complete,
            user_oid=user.oid
        )

        await self.task_repository.create_task(task=new_task)
        await self._mediator.publish(new_task.pull_events())

        return new_task


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
            raise UserNotFoundByIdException(user_oid=command.user_oid)

        task = await self.task_repository.get_task_by_oid(task_oid=command.task_oid)

        if not task:
            raise TaskNotFoundException(task_oid=command.task_oid)

        if not task.user_oid == command.user_oid:
            raise TaskAccessDeniedException()

        await self.task_repository.delete_task(task_oid=command.task_oid)


@dataclass(frozen=True)
class CompleteTaskCommand(BaseCommand):
    task_oid: str
    user_oid: str


@dataclass(frozen=True)
class CompleteTaskCommandHandler(BaseCommandHandler):
    task_repository: BaseTaskRepository
    user_repository: BaseUserRepository

    async def handle(self, command: CompleteTaskCommand) -> None:
        user = await self.user_repository.get_user_by_oid(user_oid=command.user_oid)

        if not user:
            raise UserNotFoundByIdException(user_oid=command.user_oid)

        task = await self.task_repository.get_task_by_oid(task_oid=command.task_oid)

        if not task:
            raise TaskNotFoundException(task_oid=command.task_oid)

        if task.user_oid != user.oid:
            raise TaskAccessDeniedException()

        task.complete_task()
        await self._mediator.publish(task.pull_events())

        await self.task_repository.complete_user_task(
            task_oid=command.task_oid,
            user_oid=command.user_oid
        )


@dataclass(frozen=True)
class EditTaskCommand(BaseCommand):
    task_oid: str
    user_oid: str
    title: str | None
    task_body: str | None
    time_limit: datetime.date | None


@dataclass(frozen=True)
class EditTaskCommandHandler(BaseCommandHandler[EditTaskCommand, None]):
    task_repository: BaseTaskRepository
    user_repository: BaseUserRepository

    async def handle(self, command: EditTaskCommand) -> None:
        user = await self.user_repository.get_user_by_oid(user_oid=command.user_oid)

        if not user:
            raise UserNotFoundByIdException(user_oid=command.user_oid)

        task = await self.task_repository.get_task_by_oid(task_oid=command.task_oid)

        if not task:
            raise TaskNotFoundException(task_oid=command.task_oid)

        if task.user_oid != user.oid:
            raise TaskAccessDeniedException()

        title = None if command.title is None else Title(command.title)
        task_body = None if command.task_body is None else TaskBody(command.task_body)
        time_to_complete = None if command.time_limit is None else TimeToComplete((command.time_limit - datetime.date.today()).total_seconds())

        task.update_task(
            title=title,
            task_body=task_body,
            time_to_complete=time_to_complete
        )
        await self._mediator.publish(task.pull_events())

        await self.task_repository.edit_task(
            task_oid=command.task_oid,
            user_oid=command.user_oid,
            title=title,
            task_body=task_body,
            time_to_complete=time_to_complete
        )
