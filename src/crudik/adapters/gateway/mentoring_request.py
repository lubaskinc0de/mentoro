from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from crudik.application.gateway.mentoring_request import MentoringRequestGateway
from crudik.models.mentor import Mentor
from crudik.models.mentoring_request import MentoringRequest
from crudik.models.student import Student


class MentoringRequestGatewayImpl(MentoringRequestGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def read_all_by_student(self, student_id: UUID) -> list[MentoringRequest]:
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

    async def get_by_id(self, unique_id: UUID) -> MentoringRequest | None:
        stmt = select(MentoringRequest).where(MentoringRequest.id == unique_id)
        result = await self._session.execute(stmt)
        return result.scalar()
