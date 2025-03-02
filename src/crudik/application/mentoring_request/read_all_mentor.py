from dataclasses import dataclass

from crudik.adapters.idp import TokenMentorIdProvider, UnauthorizedError
from crudik.application.data_model.mentor import convert_mentor_to_dto
from crudik.application.data_model.mentoring_request import MentoringRequestData
from crudik.application.gateway.mentoring_request import MentoringRequestGateway
from crudik.application.gateway.student_gateway import StudentGateway


@dataclass(frozen=True, slots=True)
class ReadMentorMentoringRequests:
    student_gateway: StudentGateway
    gateway: MentoringRequestGateway
    id_provider: TokenMentorIdProvider

    async def execute(self) -> list[MentoringRequestData]:
        mentor_id = await self.id_provider.get_mentor_id()
        mentor = await self.student_gateway.get_by_id(mentor_id)
        if mentor is None:
            raise UnauthorizedError

        data = await self.gateway.read_all_by_mentor(mentor_id)
        return [
            MentoringRequestData(
                id=_.id,
                type=_.type,
                created_at=_.created_at,
                mentor=convert_mentor_to_dto(_.mentor),
            )
            for _ in data
        ]
