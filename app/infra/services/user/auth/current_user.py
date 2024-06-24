from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from punq import Container


from application.api.users.schemas import UserDetailSchema
from domain.exceptions.base import ApplicationException
from logic.commands.users import GetCurrentUserCommand
from logic.init import get_container
from logic.mediator.base import Mediator

oauth2_scheme = (OAuth2PasswordBearer(tokenUrl="/auth/token"))


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        container: Container = Depends(get_container)
):
    mediator: Mediator = container.resolve(Mediator)

    try:
        user, *_ = await mediator.handle_command(
            GetCurrentUserCommand(
                token=token
            )
        )
    except ApplicationException as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': error.message})

    return UserDetailSchema(
        username=user.username.as_generic_type(),
        email=user.email.as_generic_type(),
        oid=user.oid
    )
