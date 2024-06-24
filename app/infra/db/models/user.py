import datetime

from sqlalchemy import String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infra.db.models.base import Base


class Users(Base):
    __tablename__ = "Users"

    id: Mapped[str] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(256))
    password: Mapped[str] = mapped_column(String())

    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))

    task: Mapped[list["Tasks"]] = relationship(
        back_populates='user'
    )
