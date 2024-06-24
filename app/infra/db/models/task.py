import datetime

from sqlalchemy import String, text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infra.db.models.base import Base


class Tasks(Base):
    __tablename__ = "Tasks"

    id: Mapped[str] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(80))
    task_body: Mapped[str] = mapped_column(String())
    importance: Mapped[int] = mapped_column(Integer())

    user_id: Mapped[str] = mapped_column(ForeignKey("Users.id"))
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))

    user: Mapped["Users"] = relationship(
        back_populates='task'
    )
