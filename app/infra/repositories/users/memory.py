from dataclasses import dataclass, field

from domain.entities.users import User
from infra.repositories.users.base import BaseUserRepository


@dataclass
class MemoryUserRepository(BaseUserRepository):
    _saved_users: list[User] = field(
        default_factory=list,
        kw_only=True
    )

    async def check_user_by_email(self, email: str) -> bool:
        try:
            return bool(next(
                user for user in self._saved_users if user.email.as_generic_type() == email
            ))
        except StopIteration:
            return False

    async def get_user(self, user_oid: str) -> User:
        for user in self._saved_users:
            if user.oid == user_oid:
                return user

    async def register_user(self, new_user: User) -> None:
        self._saved_users.append(new_user)

