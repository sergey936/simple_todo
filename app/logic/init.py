from functools import lru_cache

from punq import Container, Scope

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from domain.events.users import NewUserCreatedEvent
from domain.services.user.password.base import BasePasswordManager
from domain.services.user.password.password import PasswordManager
from infra.db.manager.base import BaseDatabaseManager
from infra.db.manager.postgre import PostgresDatabaseManager
from infra.notificators.base import BaseNotificator
from infra.notificators.email import EmailNotificator
from infra.repositories.tasks.base import BaseTaskRepository
from infra.repositories.tasks.postgres import PostgresTaskRepository
from infra.repositories.users.base import BaseUserRepository

from infra.repositories.users.postgres import PostgresUserRepository
from logic.commands.auth import (
    CreateAccessTokenCommandHandler, AuthenticateUserCommand,
    AuthenticateUserCommandHandler, CreateAccessTokenCommand
)
from logic.commands.tasks import CreateTaskCommand, CreateTaskCommandHandler, DeleteTaskCommandHandler, \
    DeleteTaskCommand, CompleteTaskCommandHandler, CompleteTaskCommand
from logic.commands.users import (
    CreateUserCommand, CreateUserCommandHandler, DeleteUserCommandHandler, DeleteUserCommand
)
from logic.events.users import NewUserCreatedEventHandler
from logic.mediator.base import Mediator
from logic.queries.tasks import GetAllUserTasksQueryHandler, GetAllUserTasksQuery, GetUserTaskByOidQuery, \
    GetUserTaskByOidQueryHandler
from logic.queries.users import GetUserByEmailQueryHandler, GetCurrentUserQueryHandler, GetCurrentUserQuery, \
    GetUserByEmailQuery
from settings.config import Config


@lru_cache(1)
def get_container() -> Container:
    return init_container()


def init_container() -> Container:
    container = Container()

    # register Config
    container.register(Config, instance=Config(), scope=Scope.singleton)
    config: Config = container.resolve(Config)

    # register Notificators
    def init_email_notificator() -> BaseNotificator:
        return EmailNotificator(
            smtp_server=config.smpt_server,
            smtp_port=config.smpt_port,
            smtp_username=config.smpt_user,
            smtp_password=config.smpt_password,
        )

    container.register(BaseNotificator, factory=init_email_notificator, scope=Scope.singleton)

    # register Repositories
    def init_postgres_database_manager() -> BaseDatabaseManager:
        engine = create_async_engine(config.database_url, echo=True, future=True)

        return PostgresDatabaseManager(
            _session_maker=async_sessionmaker(
                engine,
                class_=AsyncSession,
                expire_on_commit=False
            )
        )

    container.register(BaseDatabaseManager, factory=init_postgres_database_manager, scope=Scope.singleton)

    def init_postgres_task_repository() -> BaseTaskRepository:
        return PostgresTaskRepository(
            _database_manager=container.resolve(BaseDatabaseManager)
        )

    def init_postgres_user_repository() -> BaseUserRepository:
        return PostgresUserRepository(
            _database_manager=container.resolve(BaseDatabaseManager)
        )

    container.register(BaseUserRepository, factory=init_postgres_user_repository, scope=Scope.singleton)
    container.register(BaseTaskRepository, factory=init_postgres_task_repository, scope=Scope.singleton)

    # register password hasher
    container.register(BasePasswordManager, instance=PasswordManager(), scope=Scope.singleton)

    # init mediator
    def init_mediator() -> Mediator:
        mediator = Mediator()

        # initialize handlers for commands
        # User handlers command handlers
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
            config=config
        )
        delete_user_command_handler = DeleteUserCommandHandler(
            _mediator=mediator,
            user_repository=container.resolve(BaseUserRepository)
        )
        # Task command handlers
        create_task_command_handler = CreateTaskCommandHandler(
            _mediator=mediator,
            task_repository=container.resolve(BaseTaskRepository),
            user_repository=container.resolve(BaseUserRepository)
        )
        delete_user_task_command_handler = DeleteTaskCommandHandler(
            _mediator=mediator,
            task_repository=container.resolve(BaseTaskRepository),
            user_repository=container.resolve(BaseUserRepository)
        )
        complete_user_task_command_handler = CompleteTaskCommandHandler(
            _mediator=mediator,
            task_repository=container.resolve(BaseTaskRepository),
            user_repository=container.resolve(BaseUserRepository)
        )

        # initialize handlers for queries
        # Users
        get_current_user_query_handler = GetCurrentUserQueryHandler(
            user_repository=container.resolve(BaseUserRepository),
            config=container.resolve(Config)
        )
        get_user_by_email_query_handler = GetUserByEmailQueryHandler(
            user_repository=container.resolve(BaseUserRepository)
        )
        # Tasks
        get_all_user_tasks_query_handler = GetAllUserTasksQueryHandler(
            task_repository=container.resolve(BaseTaskRepository),
            user_repository=container.resolve(BaseUserRepository)
        )
        get_user_task_by_oid_query_handler = GetUserTaskByOidQueryHandler(
            task_repository=container.resolve(BaseTaskRepository),
            user_repository=container.resolve(BaseUserRepository)
        )

        # initialize handlers for events
        # Users
        new_user_created_event_handler = NewUserCreatedEventHandler(
            email_notificator=container.resolve(BaseNotificator)
        )

        # register handlers for commands
        # Users
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
            DeleteUserCommand,
            [delete_user_command_handler]
        )
        # Tasks
        mediator.register_command(
            CreateTaskCommand,
            [create_task_command_handler]
        )
        mediator.register_command(
            DeleteTaskCommand,
            [delete_user_task_command_handler]
        )
        mediator.register_command(
            CompleteTaskCommand,
            [complete_user_task_command_handler]
        )

        # register handlers for queries
        # Users
        mediator.register_query(
            GetCurrentUserQuery,
            get_current_user_query_handler
        )
        mediator.register_query(
            GetUserByEmailQuery,
            get_user_by_email_query_handler
        )
        # Tasks
        mediator.register_query(
            GetAllUserTasksQuery,
            get_all_user_tasks_query_handler
        )
        mediator.register_query(
            GetUserTaskByOidQuery,
            get_user_task_by_oid_query_handler
        )

        # register handlers for events
        # Users
        mediator.register_event(
            NewUserCreatedEvent,
            [new_user_created_event_handler]
        )

        return mediator

    container.register(Mediator, factory=init_mediator, scope=Scope.singleton)

    return container
