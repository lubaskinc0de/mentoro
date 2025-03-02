from dataclasses import dataclass

from crudik.adapters.idp import TokenStudentIdProvider, UnauthorizedError
from crudik.application.common.uow import UoW
from crudik.application.data_model.mentor import MentorData, convert_mentors_to_dto
from crudik.application.gateway.mentor_gateway import MentorGateway
from crudik.application.gateway.student_gateway import StudentGateway


@dataclass(slots=True, frozen=True)
class FindMentor:
    student_gateway: StudentGateway
    mentor_gateway: MentorGateway
    idp: TokenStudentIdProvider
    uow: UoW

    async def execute(self) -> list[MentorData]:
        student = await self.student_gateway.get_by_id(await self.idp.get_student_id())
        if student is None:
            raise UnauthorizedError

        match = await self.mentor_gateway.get_match(student.id)
        mentors: list[MentorData] = convert_mentors_to_dto(match)
        return mentors
