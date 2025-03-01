from uuid import UUID

from sqlalchemy import any_, delete, desc, exists, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from crudik.application.mentor.gateway import MentorGateway
from crudik.models.mentor import MatchHistory, Mentor, MentorSkill
from crudik.models.student import Student


class MentorGatewayImpl(MentorGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, unique_id: UUID) -> Mentor | None:
        q = select(Mentor).where(Mentor.id == unique_id)
        res = await self._session.execute(q)
        return res.scalar()

    async def get_by_name(self, name: str) -> Mentor | None:
        q = select(Mentor).where(Mentor.full_name == name)
        res = await self._session.execute(q)
        return res.scalar()

    async def get_match(self, student_id: UUID, threshold: float = 0.45) -> Mentor | None:
        mentor_history_cte = (
            select(MatchHistory.mentor_id).where(MatchHistory.student_id == student_id).cte("mentor_history_cte")
        )
        query = (
            select(
                Mentor,
            )
            .join(MentorSkill, Mentor.id == MentorSkill.mentor_id)
            .join(Student, Student.id == student_id)
            .where(
                or_(
                    MentorSkill.text == any_(Student.interests),
                    func.array_to_string(Student.interests, " ") % MentorSkill.text,
                ),
                ~exists().where(Mentor.id == mentor_history_cte.c.mentor_id),
            )
            .group_by(Mentor.id)
            .having(
                func.sum(func.similarity(MentorSkill.text, func.array_to_string(Student.interests, " "))) >= threshold,
            )
            .order_by(desc(func.sum(func.similarity(MentorSkill.text, func.array_to_string(Student.interests, " ")))))
            .limit(1)
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
