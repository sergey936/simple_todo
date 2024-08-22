from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.entities.users import User
from domain.values.users import Password, Username, Email


@dataclass
class BaseUserRepository(ABC):

    @abstractmethod
    async def get_user_by_oid(self, user_oid: str) -> User | None:
        ...

    @abstractmethod
    async def register_user(self, new_user: User) -> None:
        ...

    @abstractmethod
    async def check_user_by_email(self, email: str) -> bool:
        ...

    @abstractmethod
    async def get_user_by_email(self, email: str) -> User | None:
        ...

    @abstractmethod
    async def delete_user(self, user_oid: str) -> None:
        ...

    @abstractmethod
    async def edit_user(
            self,
            password: Password,
            username: Username,
            email: Email,
            user_oid: str
    ):
        ...
