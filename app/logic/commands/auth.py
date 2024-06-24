from dataclasses import dataclass
from datetime import datetime, timezone, timedelta

import jwt

from domain.entities.users import User
from domain.services.user.password.base import BasePasswordManager
from infra.repositories.users.base import BaseUserRepository
from logic.commands.base import BaseCommand, BaseCommandHandler
from logic.exceptions.users import WrongPasswordException, IncorrectEmailOrPasswordException
from settings.config import Config


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
            raise IncorrectEmailOrPasswordException()

        if not self.password_hasher.verify_password(
                raw_password=command.password,
                hashed_password=user.password.as_generic_type()
        ):
            raise WrongPasswordException()

        return user


@dataclass(frozen=True)
class CreateAccessTokenCommand(BaseCommand):
    data: dict


@dataclass(frozen=True)
class CreateAccessTokenCommandHandler(BaseCommandHandler):
    config: Config

    async def handle(self, command: CreateAccessTokenCommand) -> str:

        expires_delta = timedelta(minutes=self.config.token_expire_min)
        to_encode = command.data.copy()

        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.config.secret_key, algorithm=self.config.algorithm)

        return encoded_jwt
