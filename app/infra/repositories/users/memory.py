from dataclasses import dataclass, field

from domain.entities.users import User
from domain.values.users import Email, Password, Username
from infra.repositories.users.base import BaseUserRepository


@dataclass
class MemoryUserRepository(BaseUserRepository):
    _saved_users: list[User] = field(
        default_factory=list,
        kw_only=True
    )

    async def get_user(self, user_oid: str) -> User:
        for user in self._saved_users:
            if user.oid == user_oid:
                return user

    async def register_user(self, username: Username, email: Email, password: Password) -> User:
        user = User(
            username=username,
            email=email,
            password=password
        )
        self._saved_users.append(user)
