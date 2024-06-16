import jwt

from dataclasses import dataclass
from datetime import timedelta, datetime, timezone

from fastapi import HTTPException, status
from jwt import InvalidTokenError

from domain.entities.users import User
from domain.services.user.password.base import BasePasswordManager

from domain.values.users import Username, Password, Email
from infra.repositories.users.base import BaseUserRepository
from logic.commands.base import BaseCommand, BaseCommandHandler
from logic.exceptions.users import UserWithThatEmailAlreadyExists, WrongPasswordException, UserNotFound
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

        new_user = User(
            password=password,
            username=username,
            email=email
        )

        await self.user_repository.register_user(new_user=new_user)

        return new_user


@dataclass(frozen=True)
class AuthenticateUserCommand(BaseCommand):
    email: str
    password: str


@dataclass(frozen=True)
class AuthenticateUserCommandHandler(BaseCommandHandler):
    user_repository: BaseUserRepository
    password_hasher: BasePasswordManager

    async def handle(self, command: AuthenticateUserCommand) -> User:
        user = await self.user_repository.get_user_by_email(email=command.email)

        if not user:
            raise UserNotFound(text=command.email)

        if not self.password_hasher.verify_password(
            raw_password=command.password,
            hashed_password=user.password.as_generic_type()
        ):
            raise WrongPasswordException()

        return user


@dataclass(frozen=True)
class CreateAccessTokenCommand(BaseCommand):
    data: dict
    expires_delta: timedelta | None = None


@dataclass(frozen=True)
class CreateAccessTokenCommandHandler(BaseCommandHandler):
    config: Config

    async def handle(self, command: CreateAccessTokenCommand) -> str:
        to_encode = command.data.copy()

        if command.expires_delta:
            expire = datetime.now(timezone.utc) + command.expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.config.secret_key, algorithm=self.config.algorithm)

        return encoded_jwt


@dataclass(frozen=True)
class GetCurrentUserCommand(BaseCommand):
    token: str


@dataclass(frozen=True)
class GetCurrentUserCommandHandler(BaseCommandHandler):
    user_repository: BaseUserRepository
    config: Config

    async def handle(self, command: GetCurrentUserCommand):
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
