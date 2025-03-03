from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from crudik.models.base import Base
from crudik.models.mentor import Mentor
from crudik.models.student import Student


class MentoringRequestType(Enum):
    REVIEW = "review"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class MentoringRequest(Base):
    __tablename__ = "mentoring_request"

    id: Mapped[UUID] = mapped_column(nullable=False, primary_key=True, default=uuid4)
    mentor_id: Mapped[UUID] = mapped_column(ForeignKey("mentor.id"), nullable=False)
    student_id: Mapped[UUID] = mapped_column(ForeignKey("student.id"), nullable=False)
    type: Mapped[MentoringRequestType] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True, server_default=func.now())

    mentor: Mapped[Mentor] = relationship(Mentor, uselist=False)
    student: Mapped[Student] = relationship(Student, uselist=False)

    __table_args__ = (UniqueConstraint("student_id", "mentor_id"),)
