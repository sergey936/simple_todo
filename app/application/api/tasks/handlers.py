from typing import List

from fastapi import APIRouter, status, Depends, HTTPException
from punq import Container

from application.api.tasks.filters import GetTasksFilters
from application.api.tasks.schemas import TaskDetailSchema, TaskCreateSchema, GetTasksQueryResponseSchema
from application.api.users.schemas import ErrorSchema
from domain.entities.users import User
from domain.exceptions.base import ApplicationException
from infra.services.user.auth.current_user import get_current_user
from logic.commands.tasks import CreateTaskCommand
from logic.init import get_container
from logic.mediator.base import Mediator
from logic.queries.tasks import GetAllUserTasksQuery

router = APIRouter(tags=['task'])


@router.post(
    '/create',
    response_model=TaskDetailSchema,
    status_code=status.HTTP_201_CREATED,
    description='Create task for current authenticated user',
    responses={
        status.HTTP_201_CREATED: {'model': TaskDetailSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def create_task(
        task_schema: TaskCreateSchema,
        container: Container = Depends(get_container),
        current_user: User = Depends(get_current_user)
) -> TaskDetailSchema:
    mediator: Mediator = container.resolve(Mediator)

    try:
        task, *_ = await mediator.handle_command(
            CreateTaskCommand(
                title=task_schema.title,
                task_body=task_schema.task_body,
                importance=task_schema.importance,
                user_oid=current_user.oid
            )
        )
    except ApplicationException as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': error.message})

    return TaskDetailSchema.from_entity(task=task)


@router.get(
    '/user{user_oid}/my-tasks',
    response_model=GetTasksQueryResponseSchema,
    status_code=status.HTTP_200_OK,
    description='Get all current authenticated user tasks',
    responses={
        status.HTTP_200_OK: {'model': GetTasksQueryResponseSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def get_all_user_tasks(
        user_oid: str,
        filters: GetTasksFilters = Depends(),
        container: Container = Depends(get_container),
        current_user: User = Depends(get_current_user)
) -> GetTasksQueryResponseSchema:
    mediator: Mediator = container.resolve(Mediator)

    try:
        tasks, count = await mediator.handle_query(
            GetAllUserTasksQuery(
                user_oid=user_oid,
                current_user_oid=current_user.oid,
                filters=filters
            )
        )

    except ApplicationException as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': error.message})

    return GetTasksQueryResponseSchema(
        count=count,
        limit=filters.limit,
        offset=filters.offset,
        items=[TaskDetailSchema.from_entity(task) for task in tasks]
    )

