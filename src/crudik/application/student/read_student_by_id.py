from dataclasses import dataclass
from uuid import UUID

from crudik.adapters.idp import TokenMentorIdProvider, UnauthorizedError
from crudik.application.data_model.student import StudentData, convert_student_model_to_dto
from crudik.application.errors.student_errors import StudentDoesNotExistsError
from crudik.application.gateway.mentor_gateway import MentorGateway
from crudik.application.gateway.student_gateway import StudentGateway


@dataclass(slots=True, frozen=True)
class ReadStudentById:
    student_gateway: StudentGateway
    mentor_gateway: MentorGateway
    idp: TokenMentorIdProvider

    async def execute(self, student_id: UUID) -> StudentData:
        mentor = await self.mentor_gateway.get_by_id(await self.idp.get_mentor_id())
        if mentor is None:
            raise UnauthorizedError

        student = await self.student_gateway.get_by_id(student_id)
        if student is None:
            raise StudentDoesNotExistsError

        return convert_student_model_to_dto(student)
