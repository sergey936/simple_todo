from dataclasses import dataclass

from sqlalchemy import text, select, delete
from sqlalchemy.ext.asyncio import async_sessionmaker

from domain.entities.users import User
from infra.db.manager.base import BaseDatabaseManager
from infra.db.models.user import Users
from infra.repositories.converters.users.converters import convert_user_entity_to_dbmodel, \
    convert_user_db_model_to_entity
from infra.repositories.users.base import BaseUserRepository


@dataclass
class PostgresUserRepository(BaseUserRepository):
    _database_manager: BaseDatabaseManager

    @property
    async def get_session(self) -> async_sessionmaker:
        return await self._database_manager.get_sessionmaker()

    async def register_user(self, new_user: Users) -> None:
        session = await self.get_session

        async with session.begin() as session:
            session.add(new_user)

            await session.commit()

    async def check_user_by_email(self, email: str) -> bool:
        session = await self.get_session

        async with session.begin() as session:
            query = select(Users).where(Users.email == email)
            result = await session.execute(query)
            user = result.scalars().all()

            if user:
                return True

        return False

    async def get_user_by_email(self, email: str) -> User | None:
        session = await self.get_session

        async with session.begin() as session:
            query = select(Users).where(Users.email == email)
            result = await session.execute(query)
            user = result.scalars().one_or_none()

            if not user:
                return None

            return convert_user_db_model_to_entity(user=user)

    async def get_user_by_oid(self, user_oid: str) -> User | None:
        session = await self.get_session

        async with session.begin() as session:
            query = select(Users).where(Users.id == user_oid)
            result = await session.execute(query)
            user = result.scalars().one_or_none()

            if not user:
                return None

            return convert_user_db_model_to_entity(user=user)

    async def delete_user(self, user_oid: str) -> None:
        session = await self.get_session

        async with session.begin() as session:
            query = delete(Users).where(Users.id == user_oid)
            await session.execute(query)
            await session.commit()
