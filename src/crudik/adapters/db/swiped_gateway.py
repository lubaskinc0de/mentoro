from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from crudik.application.gateway.swiped_gateway import SwipedMentorGateway
from crudik.models.mentor import Mentor
from crudik.models.student import Student
from crudik.models.swiped_mentor import SwipedMentor, SwipedMentorType


class SwipedMentorGatewayImpl(SwipedMentorGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_all(
        self,
        student_id: UUID,
        swiped_mentor_type: SwipedMentorType,
    ) -> list[SwipedMentor]:
        stmt = (
            select(SwipedMentor)
            .where(Student.id == student_id, SwipedMentor.type == swiped_mentor_type)
            .join(Student, SwipedMentor.student_id == Student.id)
            .options(
                selectinload(SwipedMentor.mentor).selectinload(Mentor.skills),
                selectinload(SwipedMentor.mentor).selectinload(Mentor.contacts),
            )
            .order_by(SwipedMentor.created_at)
        )
        result = await self._session.execute(stmt)
        data = result.scalars().all()
        return list(data)

    async def read(self, student_id: UUID, mentor_id: UUID) -> SwipedMentor | None:
        stmt = select(SwipedMentor).where(SwipedMentor.student_id == student_id, SwipedMentor.mentor_id == mentor_id)
        result = await self._session.execute(stmt)
        return result.scalar()
