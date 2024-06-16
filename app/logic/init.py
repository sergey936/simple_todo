from functools import lru_cache
from punq import Container, Scope

from domain.services.user.password.base import BasePasswordManager
from domain.services.user.password.password import PasswordManager
from infra.repositories.users.base import BaseUserRepository
from infra.repositories.users.memory import MemoryUserRepository
from logic.commands.users import CreateUserCommand, CreateUserCommandHandler, AuthenticateUserCommandHandler, \
    AuthenticateUserCommand, CreateAccessTokenCommandHandler, CreateAccessTokenCommand, GetCurrentUserCommandHandler, \
    GetCurrentUserCommand
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
    container.register(BasePasswordManager, instance=PasswordManager(), scope=Scope.singleton)

    # init mediator
    def init_mediator() -> Mediator:
        mediator = Mediator()

        # initialize handlers for commands
        create_user_command_handler = CreateUserCommandHandler(
            _mediator=mediator,
            user_repository=container.resolve(BaseUserRepository),
            password_hasher=container.resolve(BasePasswordManager)
        )
        authenticate_user_command_handler = AuthenticateUserCommandHandler(
            _mediator=mediator,
            user_repository=container.resolve(BaseUserRepository),
            password_hasher=container.resolve(BasePasswordManager)
        )
        create_access_token_command_handler = CreateAccessTokenCommandHandler(
            _mediator=mediator,
            config=container.resolve(Config)
        )
        get_current_user_command_handler = GetCurrentUserCommandHandler(
            _mediator=mediator,
            user_repository=container.resolve(BaseUserRepository),
            config=container.resolve(Config)
        )

        # register handlers for commands
        mediator.register_command(
            CreateUserCommand,
            [create_user_command_handler]
        )
        mediator.register_command(
            AuthenticateUserCommand,
            [authenticate_user_command_handler]
        )
        mediator.register_command(
            CreateAccessTokenCommand,
            [create_access_token_command_handler]
        )
        mediator.register_command(
            GetCurrentUserCommand,
            [get_current_user_command_handler]
        )

        return mediator

    container.register(Mediator, factory=init_mediator, scope=Scope.singleton)

    return container

