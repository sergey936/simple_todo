import datetime
from typing import List

from sqlalchemy import String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infra.db.models.base import Base
from infra.db.models.task import Tasks


class Users(Base):
    __tablename__ = "Users"

    id: Mapped[str] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(256))
    password: Mapped[str] = mapped_column(String())

    created_at: Mapped[datetime.datetime] = mapped_column()

    task: Mapped[List["Tasks"]] = relationship("Tasks", back_populates="user")
