from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from crudik.models.base import Base


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
