from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.entities.users import User


@dataclass
class BaseUserRepository(ABC):

    @abstractmethod
    async def get_user(self, user_oid: str) -> User:
        ...
