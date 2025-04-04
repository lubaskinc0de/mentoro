from datetime import datetime
from uuid import UUID

from sqlalchemy import ARRAY, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from crudik.models.base import Base


class Student(Base):
    __tablename__ = "student"

    id: Mapped[UUID] = mapped_column(primary_key=True, nullable=False)
    full_name: Mapped[str] = mapped_column(nullable=False, unique=True)
    age: Mapped[int | None] = mapped_column(nullable=True)
    interests: Mapped[list[str]] = mapped_column(ARRAY(String, dimensions=1), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    avatar_url: Mapped[str | None] = mapped_column()
    description: Mapped[str | None] = mapped_column()
