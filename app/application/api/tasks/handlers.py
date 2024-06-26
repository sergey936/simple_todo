from fastapi import APIRouter, status, Depends, HTTPException
from punq import Container

from application.api.tasks.filters import GetTasksFilters
from application.api.tasks.schemas import TaskDetailSchema, TaskCreateSchema, GetTasksQueryResponseSchema, \
    DeleteTaskSchema, CompleteTaskSchema
from application.api.users.schemas import ErrorSchema
from domain.entities.users import User
from domain.exceptions.base import ApplicationException
from infra.services.user.auth.current_user import get_current_user
from logic.commands.tasks import CreateTaskCommand, DeleteTaskCommand, CompleteTaskCommand
from logic.init import get_container
from logic.mediator.base import Mediator
from logic.queries.tasks import GetAllUserTasksQuery, GetUserTaskByOidQuery

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
        filters: GetTasksFilters = Depends(),
        container: Container = Depends(get_container),
        current_user: User = Depends(get_current_user)
) -> GetTasksQueryResponseSchema:
    mediator: Mediator = container.resolve(Mediator)

    try:
        tasks, count = await mediator.handle_query(
            GetAllUserTasksQuery(
                user_oid=current_user.oid,
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


@router.get(
    '/{task_oid}',
    response_model=TaskDetailSchema,
    status_code=status.HTTP_200_OK,
    description='Get user task by task_oid',
    responses={
        status.HTTP_200_OK: {'model': TaskDetailSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def get_user_task_by_oid(
        task_oid: str,
        container: Container = Depends(get_container),
        current_user: User = Depends(get_current_user)
) -> TaskDetailSchema:
    mediator: Mediator = container.resolve(Mediator)

    try:
        task = await mediator.handle_query(
            GetUserTaskByOidQuery(
                user_oid=current_user.oid,
                task_oid=task_oid
            )
        )

    except ApplicationException as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': error.message})

    return TaskDetailSchema.from_entity(task=task)


@router.delete(
    '/delete/{task_oid}',
    response_model=DeleteTaskSchema,
    status_code=status.HTTP_200_OK,
    description='Delete user task by task_oid',
    responses={
        status.HTTP_200_OK: {'model': DeleteTaskSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def delete_user_task(
        task_oid: str,
        container: Container = Depends(get_container),
        current_user: User = Depends(get_current_user)
) -> DeleteTaskSchema:
    mediator: Mediator = container.resolve(Mediator)

    try:
        await mediator.handle_command(
            DeleteTaskCommand(
                task_oid=task_oid,
                user_oid=current_user.oid
            )
        )

    except ApplicationException as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': error.message})

    return DeleteTaskSchema


@router.put(
    '/make-complete/{task_oid}',
    response_model=CompleteTaskSchema,
    status_code=status.HTTP_200_OK,
    description='Complete user task by task_oid',
    responses={
        status.HTTP_200_OK: {'model': CompleteTaskSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def complete_user_task(
        task_oid: str,
        container: Container = Depends(get_container),
        current_user: User = Depends(get_current_user)
) -> CompleteTaskSchema:
    mediator: Mediator = container.resolve(Mediator)

    try:
        await mediator.handle_command(
            CompleteTaskCommand(
                task_oid=task_oid,
                user_oid=current_user.oid
            )
        )

    except ApplicationException as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': error.message})

    return CompleteTaskSchema
