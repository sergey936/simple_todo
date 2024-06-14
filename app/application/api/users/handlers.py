from fastapi import APIRouter, Depends, HTTPException, status
from punq import Container

from domain.exceptions.base import ApplicationException
from logic.commands.users import CreateUserCommand
from logic.init import init_container
from logic.mediator.base import Mediator

router = APIRouter(tags=['user'])


@router.get('/test')
async def register():
    return {'response': 'working'}


@router.post('/register')
async def register(
        password: str,
        email: str,
        username: str,
        container: Container = Depends(init_container)
):
    mediator = container.resolve(Mediator)

    try:
        new_user = await mediator.handle_command(
            CreateUserCommand(
                password=password,
                email=email,
                username=username,
            )
        )
    except ApplicationException as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': error.message})

    return new_user
