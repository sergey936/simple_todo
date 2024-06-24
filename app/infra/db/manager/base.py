from abc import ABC, abstractmethod
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import async_sessionmaker


@dataclass
class BaseDatabaseManager(ABC):
    @abstractmethod
    async def get_sessionmaker(self) -> async_sessionmaker:
        ...


