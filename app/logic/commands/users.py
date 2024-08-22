from dataclasses import dataclass

from domain.entities.users import User
from domain.services.user.password.base import BasePasswordManager

from domain.values.users import Username, Password, Email
from infra.repositories.converters.users.converters import convert_user_entity_to_dbmodel
from infra.repositories.users.base import BaseUserRepository
from logic.commands.base import BaseCommand, BaseCommandHandler, CT, CR
from logic.exceptions.users import UserWithThatEmailAlreadyExists, UserNotFoundByIdException


@dataclass(frozen=True)
class CreateUserCommand(BaseCommand):
    username: str
    password: str
    email: str


@dataclass(frozen=True)
class CreateUserCommandHandler(BaseCommandHandler):
    user_repository: BaseUserRepository
    password_hasher: BasePasswordManager

    async def handle(self, command: CreateUserCommand) -> User:
        if await self.user_repository.check_user_by_email(email=command.email):
            raise UserWithThatEmailAlreadyExists(text=command.email)

        password = Password(value=self.password_hasher.hash_password(command.password))
        username = Username(value=command.username)
        email = Email(value=command.email)

        new_user = User.create_user(
            password=password,
            username=username,
            email=email
        )

        await self.user_repository.register_user(new_user=convert_user_entity_to_dbmodel(user=new_user))

        await self._mediator.publish(new_user.pull_events())

        return new_user


@dataclass(frozen=True)
class DeleteUserCommand(BaseCommand):
    user_oid: str


@dataclass(frozen=True)
class DeleteUserCommandHandler(BaseCommandHandler):
    user_repository: BaseUserRepository

    async def handle(self, command: DeleteUserCommand):
        user = await self.user_repository.get_user_by_oid(user_oid=command.user_oid)

        if not user:
            raise UserNotFoundByIdException(user_oid=command.user_oid)

        await self.user_repository.delete_user(user_oid=command.user_oid)


@dataclass(frozen=True)
class EditUserCommand(BaseCommand):
    user_oid: str
    username: str | None
    password: str | None
    email: str | None


@dataclass(frozen=True)
class EditUserCommandHandler(BaseCommandHandler[EditUserCommand, None]):
    user_repository: BaseUserRepository
    password_hasher: BasePasswordManager

    async def handle(self, command: EditUserCommand) -> None:
        user = await self.user_repository.get_user_by_oid(user_oid=command.user_oid)

        if not user:
            raise UserNotFoundByIdException(user_oid=command.user_oid)

        password = None if command.password is None else Password(value=self.password_hasher.hash_password(command.password))
        username = None if command.username is None else Username(value=command.username)
        email = None if command.email is None else Email(value=command.email)

        await self.user_repository.edit_user(
            password=password,
            username=username,
            email=email,
            user_oid=user.oid
        )
