from uuid import UUID

from sqlalchemy import and_, delete, exists, func, literal, not_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from crudik.application.mentor.gateway import MentorGateway
from crudik.models.mentor import MatchHistory, Mentor, MentorSkill
from crudik.models.student import Student


class MentorGatewayImpl(MentorGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, unique_id: UUID) -> Mentor | None:
        q = select(Mentor).where(Mentor.id == unique_id).options(joinedload(Mentor.skills, Mentor.contacts))
        res = await self._session.execute(q)
        return res.scalar()

    async def get_by_name(self, name: str) -> Mentor | None:
        q = select(Mentor).where(Mentor.full_name == name).options(joinedload(Mentor.skills, Mentor.contacts))
        res = await self._session.execute(q)
        return res.scalar()

    async def get_match(self, student_id: UUID, threshold: float = 0.45) -> Mentor | None:
        mentor_history_cte = (
            select(MatchHistory.mentor_id).where(MatchHistory.student_id == student_id).cte("mentor_history_cte")
        )

        student_interests = (
            select(func.unnest(Student.interests).label("interest"))
            .where(Student.id == student_id)
            .cte("student_interests")
        )

        query = (
            select(Mentor)
            .join(MentorSkill, Mentor.id == MentorSkill.mentor_id)
            .join(student_interests, literal(True))  # noqa: FBT003
            .where(
                and_(
                    func.similarity(MentorSkill.text, student_interests.c.interest) > 0,
                    not_(exists().where(Mentor.id == mentor_history_cte.c.mentor_id)),
                ),
            )
            .group_by(Mentor.id)
            .having(func.sum(func.similarity(MentorSkill.text, student_interests.c.interest)) >= threshold)
            .order_by(func.sum(func.similarity(MentorSkill.text, student_interests.c.interest)).desc())
            .limit(1)
            .options(selectinload(Mentor.skills, Mentor.contacts))
        )

        result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def clear_history(self, student_id: UUID) -> None:
        q = delete(MatchHistory).where(MatchHistory.student_id == student_id)
        await self._session.execute(q)

    async def exists_in_history(self, student_id: UUID, mentor_id: UUID) -> bool:
        q = select(exists(MatchHistory.student_id)).where(
            MatchHistory.student_id == student_id,
            MatchHistory.mentor_id == mentor_id,
        )
        res = await self._session.execute(q)
        return bool(res.scalar())
