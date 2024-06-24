from functools import lru_cache

from punq import Container, Scope

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker


from domain.services.user.password.base import BasePasswordManager
from domain.services.user.password.password import PasswordManager
from infra.db.manager.postgre import PostgresDatabaseManager
from infra.repositories.users.base import BaseUserRepository

from infra.repositories.users.postgres import PostgresUserRepository
from logic.commands.auth import (
    CreateAccessTokenCommandHandler, AuthenticateUserCommand,
    AuthenticateUserCommandHandler, CreateAccessTokenCommand
)
from logic.commands.users import (
    CreateUserCommand, CreateUserCommandHandler, GetCurrentUserCommand,
    GetUserByEmailHandler, GetUserByEmail, GetCurrentUserCommandHandler
)
from logic.mediator.base import Mediator
from settings.config import Config


@lru_cache(1)
def get_container() -> Container:
    return init_container()


class BaseDatabaseManger:
    pass


def init_container() -> Container:
    container = Container()

    # register Config
    container.register(Config, instance=Config(), scope=Scope.singleton)

    # register Repositories
    def init_postgres_database_manager() -> BaseDatabaseManger:
        config: Config = container.resolve(Config)
        engine = create_async_engine(config.database_url, echo=True, future=True)

        return PostgresDatabaseManager(
            _session_maker=async_sessionmaker(
                engine,
                class_=AsyncSession,
                expire_on_commit=False
            )
        )

    container.register(BaseDatabaseManger, factory=init_postgres_database_manager, scope=Scope.singleton)

    def init_postgres_user_repository() -> BaseUserRepository:
        return PostgresUserRepository(
            _database_manager=container.resolve(BaseDatabaseManger)
        )

    container.register(BaseUserRepository, factory=init_postgres_user_repository, scope=Scope.singleton)

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
        get_user_by_email_command_handler = GetUserByEmailHandler(
            _mediator=mediator,
            user_repository=container.resolve(BaseUserRepository)
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
        mediator.register_command(
            GetUserByEmail,
            [get_user_by_email_command_handler]
        )

        return mediator

    container.register(Mediator, factory=init_mediator, scope=Scope.singleton)

    return container
