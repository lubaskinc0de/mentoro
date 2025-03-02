from dataclasses import dataclass

from crudik.adapters.idp import TokenStudentIdProvider, UnauthorizedError
from crudik.application.data_model.mentoring_request import MentoringRequestData
from crudik.application.mentoring_request.gateway import MentorignRequestGateway
from crudik.application.student.gateway import StudentGateway
from crudik.application.data_model.mentor import convert_mentor_to_dto


@dataclass(frozen=True, slots=True)
class ReadAllMentoringRequest:
    student_gateway: StudentGateway
    gateway: MentorignRequestGateway
    id_provider: TokenStudentIdProvider

    async def execute(self) -> list[MentoringRequestData]:
        student_id = await self.id_provider.get_student_id()
        student = await self.student_gateway.get_by_id(student_id)
        if student is None:
            raise UnauthorizedError

        data = await self.gateway.read_all(student.id)
        return [
            MentoringRequestData(
                id=_.id,
                type=_.type,
                created_at=_.created_at,
                mentor=convert_mentor_to_dto(_.mentor),
            )
            for _ in data
        ]
