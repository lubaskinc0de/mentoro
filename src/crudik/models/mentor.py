from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from crudik.models.base import Base
from crudik.models.student import Student


class MentorSkill(Base):
    __tablename__ = "mentor_skill"

    id: Mapped[UUID] = mapped_column(primary_key=True, nullable=False)
    text: Mapped[str] = mapped_column(nullable=False)
    file_id: Mapped[UUID | None] = mapped_column(nullable=True)
    mentor_id: Mapped[UUID] = mapped_column(ForeignKey("mentor.id"))


class MentorContact(Base):
    __tablename__ = "mentor_contact"

    id: Mapped[UUID] = mapped_column(primary_key=True, nullable=False)
    url: Mapped[str] = mapped_column()
    social_network: Mapped[str] = mapped_column()
    mentor_id: Mapped[UUID] = mapped_column(ForeignKey("mentor.id"))


class Mentor(Base):
    __tablename__ = "mentor"

    id: Mapped[UUID] = mapped_column(primary_key=True, nullable=False)
    full_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    age: Mapped[int | None] = mapped_column(nullable=True)
    description: Mapped[str | None] = mapped_column(nullable=True)
    photo_url: Mapped[str | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True, server_default=func.now())
    skills: Mapped[list[MentorSkill]] = relationship(MentorSkill)
    contacts: Mapped[list[MentorContact]] = relationship(MentorContact)


class MatchHistory(Base):
    __tablename__ = "mentor_history"

    student_id: Mapped[UUID] = mapped_column(ForeignKey(Student.id), primary_key=True)
    mentor_id: Mapped[UUID] = mapped_column(ForeignKey(Mentor.id), primary_key=True)
