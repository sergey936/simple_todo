import jwt

from dataclasses import dataclass

from fastapi import HTTPException, status
from jwt import InvalidTokenError

from domain.entities.users import User
from domain.services.user.password.base import BasePasswordManager

from domain.values.users import Username, Password, Email
from infra.repositories.converters.users.converters import convert_user_entity_to_dbmodel
from infra.repositories.users.base import BaseUserRepository
from logic.commands.base import BaseCommand, BaseCommandHandler
from logic.exceptions.users import UserWithThatEmailAlreadyExists, UserNotFoundByEmailException
from settings.config import Config


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

        return new_user


@dataclass(frozen=True)
class GetCurrentUserCommand(BaseCommand):
    token: str


@dataclass(frozen=True)
class GetCurrentUserCommandHandler(BaseCommandHandler):
    user_repository: BaseUserRepository
    config: Config

    async def handle(self, command: GetCurrentUserCommand) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(command.token, self.config.secret_key, algorithms=[self.config.algorithm])
            email: str = payload.get("email")

            if not email:
                raise credentials_exception

        except InvalidTokenError:
            raise credentials_exception

        user = await self.user_repository.get_user_by_email(email=email)

        if not user:
            raise credentials_exception

        return user


@dataclass(frozen=True)
class GetUserByEmail(BaseCommand):
    email: str


@dataclass(frozen=True)
class GetUserByEmailHandler(BaseCommandHandler):
    user_repository: BaseUserRepository

    async def handle(self, command: GetUserByEmail) -> User:
        user = await self.user_repository.get_user_by_email(email=command.email)

        if not user:
            raise UserNotFoundByEmailException(email=user.email)

        return user


@dataclass(frozen=True)
class DeleteUserCommand(BaseCommand):
    user_oid: str


@dataclass(frozen=True)
class DeleteUserCommandHandler(BaseCommandHandler):
    user_repository: BaseUserRepository

    async def handle(self, command: DeleteUserCommand):
        user = await self.user_repository.get_user_by_oid(user_oid=command.user_oid)

        if not user:
            raise UserNotFoundByEmailException(email=user.email)

        await self.user_repository.delete_user(user_oid=command.user_oid)
