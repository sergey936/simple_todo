from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.entities.users import User


@dataclass
class BaseUserRepository(ABC):

    @abstractmethod
    async def get_user(self, user_oid: str) -> User:
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
