from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crudik.application.mentor.gateway import MentorGateway
from crudik.models.mentor import Mentor


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
