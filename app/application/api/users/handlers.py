from fastapi import APIRouter, Depends, HTTPException, status

from punq import Container

from application.api.users.schemas import UserDetailSchema, ErrorSchema

from domain.exceptions.base import ApplicationException
from infra.services.user.auth.current_user import get_current_user

from logic.commands.users import CreateUserCommand
from logic.init import get_container
from logic.mediator.base import Mediator


router = APIRouter(tags=['user'])


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
        password: str,
        email: str,
        username: str,
        container: Container = Depends(get_container)
) -> UserDetailSchema:
    """ Create new user """
    mediator: Mediator = container.resolve(Mediator)

    try:
        new_user, *_ = await mediator.handle_command(
            CreateUserCommand(
                password=password,
                email=email,
                username=username,
            )
        )
    except ApplicationException as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': error.message})

    return UserDetailSchema.from_entity(new_user)


@router.get('/me')
async def users_me(
        current_user: UserDetailSchema = Depends(get_current_user)
):
    return current_user

