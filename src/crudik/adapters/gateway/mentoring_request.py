from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from crudik.application.gateway.mentoring_request import MentoringRequestGateway
from crudik.models.mentor import Mentor
from crudik.models.mentoring_request import MentoringRequest


class MentoringRequestGatewayImpl(MentoringRequestGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def read_all_by_student(self, student_id: UUID) -> list[MentoringRequest]:
        stmt = (
            select(MentoringRequest)
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

    async def read_all_by_mentor(self, mentor_id: UUID) -> list[MentoringRequest]:
        stmt = (
            select(MentoringRequest)
            .join(Mentor, Mentor.id == MentoringRequest.mentor_id)
            .where(MentoringRequest.mentor_id == mentor_id)
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

    async def get_by_student_and_mentor(self, student_id: UUID, mentor_id: UUID) -> MentoringRequest | None:
        stmt = select(MentoringRequest).where(
            MentoringRequest.student_id == student_id, MentoringRequest.mentor_id == mentor_id
        )
        result = await self._session.execute(stmt)
        return result.scalar()
