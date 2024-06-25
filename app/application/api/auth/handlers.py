from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from punq import Container

from application.api.auth.schemas import TokenSchema
from application.api.users.schemas import ErrorSchema
from domain.exceptions.base import ApplicationException
from logic.commands.auth import CreateAccessTokenCommand, AuthenticateUserCommand
from logic.init import get_container
from logic.mediator.base import Mediator

router = APIRouter(tags=['auth'])


@router.post(
    "/token",
    status_code=status.HTTP_200_OK,
    description='Login with jwt token',
    responses={
        status.HTTP_200_OK: {'model': TokenSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def login_for_access_token_handler(
    form_data: OAuth2PasswordRequestForm = Depends(),
    container: Container = Depends(get_container)
) -> TokenSchema:
    """ Login with jwt """
    mediator: Mediator = container.resolve(Mediator)

    try:
        user, *_ = await mediator.handle_command(
            AuthenticateUserCommand(
                email=form_data.username,
                password=form_data.password
            )
        )

        access_token, *_ = await mediator.handle_command(
            CreateAccessTokenCommand(
                data={"email": user.email.as_generic_type()},
            )
        )

    except ApplicationException as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': error.message})

    return TokenSchema(
        access_token=access_token,
        token_type="bearer"
    )
