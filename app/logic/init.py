from functools import lru_cache
from punq import Container, Scope

from domain.services.user.password import BasePasswordHasher
from domain.services.user.password import PasswordHasher
from infra.repositories.users.base import BaseUserRepository
from infra.repositories.users.memory import MemoryUserRepository
from logic.commands.users import CreateUserCommand, CreateUserCommandHandler
from logic.mediator.base import Mediator
from settings.config import Config


@lru_cache(1)
def get_container() -> Container:
    return init_container()


def init_container() -> Container:
    container = Container()

    # register Config
    container.register(Config, instance=Config(), scope=Scope.singleton)

    # register Repositories
    container.register(BaseUserRepository, instance=MemoryUserRepository(), scope=Scope.singleton)

    # register password hasher
    container.register(BasePasswordHasher, instance=PasswordHasher(), scope=Scope.singleton)

    # init mediator
    def init_mediator() -> Mediator:
        mediator = Mediator()
        create_user_command_handler = CreateUserCommandHandler(
            _mediator=mediator,
            user_repository=container.resolve(BaseUserRepository),
            password_hasher=container.resolve(BasePasswordHasher)
        )

        mediator.register_command(CreateUserCommand, [create_user_command_handler])

        return mediator

    container.register(Mediator, factory=init_mediator, scope=Scope.singleton)

    return container

