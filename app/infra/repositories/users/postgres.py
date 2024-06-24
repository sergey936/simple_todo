from dataclasses import dataclass

from sqlalchemy import text

from domain.entities.users import User
from infra.db.manager.base import BaseDatabaseManager
from infra.repositories.users.base import BaseUserRepository


@dataclass
class PostgresUserRepository(BaseUserRepository):
    _database_manager: BaseDatabaseManager

    async def register_user(self, new_user: User) -> None:

        session = await self._database_manager.get_sessionmaker()
        async with session() as session:
            res = await session.execute(text("SELECT 1"))
            print(res.all())

    async def check_user_by_email(self, email: str) -> bool:
        return False

    async def get_user_by_email(self, email: str) -> User | None:
        ...

    async def get_user_by_oid(self, user_oid: str) -> User | None:
        ...
