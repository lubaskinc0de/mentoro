from sqlalchemy.ext.asyncio import AsyncSession

from crudik.application.student.gateway import StudentGateway
from crudik.models.student import Student


class StudentGatewayImpl(StudentGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, entity: Student) -> None:
        self._session.add(entity)
