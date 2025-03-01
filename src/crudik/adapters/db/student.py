from sqlalchemy.ext.asyncio import AsyncSession

from crudik.application.student.gateway import StudentGateway


class StudentGatewayImpl(StudentGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
