from dataclasses import dataclass

from crudik.adapters.idp import TokenStudentIdProvider, UnauthorizedError
from crudik.application.data_model.mentor import convert_mentor_to_dto
from crudik.application.data_model.mentoring_request import MentoringRequestData
from crudik.application.gateway.mentoring_request import MentoringRequestGateway
from crudik.application.gateway.student_gateway import StudentGateway
from crudik.models.mentoring_request import MentoringRequestType


@dataclass(frozen=True, slots=True)
class ReadStudentMentoringRequests:
    student_gateway: StudentGateway
    gateway: MentoringRequestGateway
    id_provider: TokenStudentIdProvider

    async def execute(self) -> list[MentoringRequestData]:
        student_id = await self.id_provider.get_student_id()
        student = await self.student_gateway.get_by_id(student_id)
        if student is None:
            raise UnauthorizedError

        data = await self.gateway.read_all_by_student(student.id)
        result = []

        for mentoring_request in data:
            mentor = convert_mentor_to_dto(mentoring_request.mentor)
            if mentoring_request.type != MentoringRequestType.ACCEPTED:
                mentor.contacts = []

            result.append(
                MentoringRequestData(
                    id=mentoring_request.id,
                    type=mentoring_request.type,
                    created_at=mentoring_request.created_at,
                    mentor=mentor,
                )
            )

        return result
