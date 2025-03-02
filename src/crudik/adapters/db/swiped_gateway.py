from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from crudik.application.swiped_mentor.gateway import SwipedMentorGateway
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
            .join(Mentor, SwipedMentor.mentor_id == Mentor.id)
            .join(Student, SwipedMentor.id == SwipedMentor.student_id)
            .where(Student.id == student_id, SwipedMentor.type == swiped_mentor_type)
            .order_by(SwipedMentor.created_at)
            .options(
                joinedload(SwipedMentor.mentor),
                joinedload(Mentor.skills),
            )
        )
        result = await self._session.execute(stmt)
        data = result.scalars().all()
        return list(data)

    async def delete(self, entity: SwipedMentor) -> None:
        stmt = delete(SwipedMentor).where(SwipedMentor.id == entity.id)
        await self._session.execute(stmt)

    async def read(self, student_id: UUID, mentor_id: UUID) -> SwipedMentor | None:
        stmt = select(SwipedMentor).where(SwipedMentor.student_id == student_id, SwipedMentor.mentor_id == mentor_id)
        result = await self._session.execute(stmt)
        return result.scalar()
