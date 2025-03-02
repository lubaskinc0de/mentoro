from dataclasses import dataclass
from uuid import UUID

from crudik.adapters.idp import TokenStudentIdProvider, UnauthorizedError
from crudik.application.data_model.mentor import MentorData, convert_mentor_to_dto
from crudik.application.errors.mentor_errors import MentorDoesNotExistsError
from crudik.application.gateway.mentor_gateway import MentorGateway
from crudik.application.gateway.student_gateway import StudentGateway


@dataclass(slots=True, frozen=True)
class ReadMentorById:
    gateway: MentorGateway
    student_gateway: StudentGateway
    idp: TokenStudentIdProvider

    async def execute(self, mentor_id: UUID) -> MentorData:
        student = await self.student_gateway.get_by_id(await self.idp.get_student_id())
        if student is None:
            raise UnauthorizedError

        mentor = await self.gateway.get_by_id(mentor_id)

        if mentor is None:
            raise MentorDoesNotExistsError

        return convert_mentor_to_dto(mentor)
