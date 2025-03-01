from datetime import datetime
from uuid import UUID

from sqlalchemy import ARRAY, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from crudik.models.base import Base


class Mentor(Base):
    __tablename__ = "mentor"

    id: Mapped[UUID] = mapped_column(primary_key=True, nullable=False)
    full_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(nullable=True)
    photo_url: Mapped[str | None] = mapped_column(nullable=True)
    contacts: Mapped[list[str]] = mapped_column(ARRAY(String, dimensions=1), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True, server_default=func.now())


class MentorSkill(Base):
    __tablename__ = "mentor_skill"

    id: Mapped[UUID] = mapped_column(primary_key=True, nullable=False)
    text: Mapped[str] = mapped_column(nullable=False)
    file_id: Mapped[UUID | None] = mapped_column(nullable=True)
    mentor_id: Mapped[UUID] = mapped_column(ForeignKey(Mentor.id))
