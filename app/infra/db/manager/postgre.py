from dataclasses import dataclass


from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from infra.db.manager.base import BaseDatabaseManager


@dataclass
class PostgresDatabaseManager(BaseDatabaseManager):
    _session_maker: async_sessionmaker

    async def get_sessionmaker(self) -> async_sessionmaker:
        return self._session_maker

