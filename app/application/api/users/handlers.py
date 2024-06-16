from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from punq import Container

from application.api.users.schemas import UserDetailSchema, ErrorSchema

from domain.exceptions.base import ApplicationException
from logic.commands.users import CreateUserCommand, CreateAccessTokenCommand, AuthenticateUserCommand, \
     GetCurrentUserCommand
from logic.init import get_container
from logic.mediator.base import Mediator
from settings.config import Config

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
async def register(
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


@router.post("/token")
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        container: Container = Depends(get_container)
):
    mediator: Mediator = container.resolve(Mediator)
    config: Config = container.resolve(Config)

    try:
        user, *_ = await mediator.handle_command(
            AuthenticateUserCommand(
                email=form_data.username,
                password=form_data.password
            )
        )
    except ApplicationException as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': error.message})

    access_token_expires = timedelta(minutes=config.token_expire_min)

    access_token, *_ = await mediator.handle_command(
        CreateAccessTokenCommand(
            data={"email": user.email.as_generic_type(), 'username': user.username.as_generic_type()},
            expires_delta=access_token_expires
        )
    )

    return access_token


# TODO глобал))) (надо как-то убрать)
test_container = get_container()
test_config = test_container.resolve(Config)


# авторизация работает только через постман
# TODO пофиксить авторизацию через свагер
@router.get("/me")
async def read_users_me(
        container: Container = Depends(get_container),
        token: str = Depends(test_config.oauth2_scheme)
):
    mediator: Mediator = container.resolve(Mediator)

    current_user = await mediator.handle_command(
        GetCurrentUserCommand(
            token=token
        )
    )

    return current_user
