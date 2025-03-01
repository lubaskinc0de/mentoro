from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crudik.application.student.gateway import StudentGateway
from crudik.models.student import Student


class StudentGatewayImpl(StudentGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, unique_id: UUID) -> Student | None:
        q = select(Student).where(Student.id == unique_id)
        res = await self._session.execute(q)
        return res.scalar()

    async def get_by_name(self, name: str) -> Student | None:
        q = select(Student).where(Student.full_name == name)
        res = await self._session.execute(q)
        return res.scalar()
