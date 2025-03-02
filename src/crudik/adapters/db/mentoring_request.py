from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from crudik.application.mentoring_request.gateway import MentorignRequestGateway
from crudik.models.mentor import Mentor
from crudik.models.mentoring_request import MentoringRequest
from crudik.models.student import Student


class MentorignRequestGatewayImpl(MentorignRequestGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def read_all(self, student_id: UUID) -> list[MentoringRequest]:
        stmt = (
            select(MentoringRequest)
            .join(Student, Student.id == MentoringRequest.student_id)
            .join(Mentor, Mentor.id == MentoringRequest.mentor_id)
            .where(MentoringRequest.student_id == student_id)
            .options(
                selectinload(MentoringRequest.mentor).selectinload(Mentor.contacts),
                selectinload(MentoringRequest.mentor).selectinload(Mentor.skills),
            )
            .order_by(MentoringRequest.created_at)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())
