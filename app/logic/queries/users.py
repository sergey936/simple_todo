from dataclasses import dataclass

import jwt
from fastapi import HTTPException, status
from jwt import InvalidTokenError

from domain.entities.users import User
from infra.repositories.users.base import BaseUserRepository
from logic.exceptions.users import UserNotFoundByEmailException
from logic.queries.base import BaseQuery, BaseQueryHandler
from settings.config import Config


@dataclass(frozen=True)
class GetCurrentUserQuery(BaseQuery):
    token: str


@dataclass(frozen=True)
class GetCurrentUserQueryHandler(BaseQueryHandler):
    user_repository: BaseUserRepository
    config: Config

    async def handle(self, query: GetCurrentUserQuery) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(query.token, self.config.secret_key, algorithms=[self.config.algorithm])
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
class GetUserByEmailQuery(BaseQuery):
    email: str


@dataclass(frozen=True)
class GetUserByEmailQueryHandler(BaseQueryHandler):
    user_repository: BaseUserRepository

    async def handle(self, query: GetUserByEmailQuery) -> User:
        user = await self.user_repository.get_user_by_email(email=query.email)

        if not user:
            raise UserNotFoundByEmailException(email=user.email)

        return user
