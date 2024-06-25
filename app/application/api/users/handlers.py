from fastapi import APIRouter, Depends, HTTPException, status

from punq import Container

from application.api.users.schemas import UserDetailSchema, ErrorSchema, UserDeleteSchema, CreateUserSchema
from domain.entities.users import User

from domain.exceptions.base import ApplicationException
from infra.services.user.auth.current_user import get_current_user

from logic.commands.users import CreateUserCommand, DeleteUserCommand
from logic.init import get_container
from logic.mediator.base import Mediator


router = APIRouter(tags=['user'])


@router.get(
    '/me',
    response_model=UserDetailSchema,
    status_code=status.HTTP_200_OK,
    description='Get info about current authenticated user',
    responses={
        status.HTTP_200_OK: {'model': UserDetailSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def users_me(
        current_user: User = Depends(get_current_user)
) -> UserDetailSchema:
    """ Info about current authenticated user """
    return UserDetailSchema.from_entity(user=current_user)


@router.post(
    '/register',
    response_model=UserDetailSchema,
    status_code=status.HTTP_201_CREATED,
    description='Creating new user, if user already exists, then return 400 error',
    responses={
        status.HTTP_201_CREATED: {'model': UserDetailSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def create_user_handler(
        user_schema: CreateUserSchema,
        container: Container = Depends(get_container)
) -> UserDetailSchema:
    """ Create new user """
    mediator: Mediator = container.resolve(Mediator)

    try:
        new_user, *_ = await mediator.handle_command(
            CreateUserCommand(
                password=user_schema.password,
                email=user_schema.email,
                username=user_schema.username,
            )
        )
    except ApplicationException as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': error.message})

    return UserDetailSchema.from_entity(new_user)


@router.delete(
    '/delete/me',
    response_model=UserDeleteSchema,
    status_code=status.HTTP_200_OK,
    description='Deleting user with that {user_oid} if authenticated',
    responses={
        status.HTTP_201_CREATED: {'model': UserDeleteSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def delete_user(
        current_user: User = Depends(get_current_user),
        container: Container = Depends(get_container)
) -> UserDeleteSchema:
    mediator: Mediator = container.resolve(Mediator)

    try:
        await mediator.handle_command(
            DeleteUserCommand(
                user_oid=current_user.oid
            )
        )
    except ApplicationException as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': error.message})

    return UserDeleteSchema

