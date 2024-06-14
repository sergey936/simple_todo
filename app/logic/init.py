from functools import lru_cache
from punq import Container, Scope
from infra.repositories.users.base import BaseUserRepository
from infra.repositories.users.memory import MemoryUserRepository
from logic.commands.users import CreateUserCommand, CreateUserCommandHandler
from logic.mediator.base import Mediator


@lru_cache(1)
def get_container() -> Container:
    return init_container()


def init_container() -> Container:
    container = Container()

    container.register(BaseUserRepository, instance=MemoryUserRepository(), scope=Scope.singleton)

    # init mediator
    def init_mediator() -> Mediator:
        mediator = Mediator()
        create_user_command_handler = CreateUserCommandHandler(
            _mediator=mediator,
            user_repository=container.resolve(BaseUserRepository)
        )

        mediator.register_command(CreateUserCommand, [create_user_command_handler])

        return mediator

    container.register(Mediator, factory=init_mediator, scope=Scope.singleton)

    return container

