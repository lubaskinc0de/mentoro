from dataclasses import dataclass

from crudik.adapters.idp import TokenMentorIdProvider, UnauthorizedError
from crudik.application.data_model.mentoring_request import MentoringRequestMentorData
from crudik.application.data_model.student import convert_student_model_to_dto
from crudik.application.gateway.mentor_gateway import MentorGateway
from crudik.application.gateway.mentoring_request import MentoringRequestGateway


@dataclass(frozen=True, slots=True)
class ReadMentorMentoringRequests:
    mentor_gateway: MentorGateway
    gateway: MentoringRequestGateway
    id_provider: TokenMentorIdProvider

    async def execute(self) -> list[MentoringRequestMentorData]:
        mentor_id = await self.id_provider.get_mentor_id()
        mentor = await self.mentor_gateway.get_by_id(mentor_id)
        if mentor is None:
            raise UnauthorizedError

        data = await self.gateway.read_all_by_mentor(mentor_id)
        return [
            MentoringRequestMentorData(
                id=_.id,
                type=_.type,
                created_at=_.created_at,
                student=convert_student_model_to_dto(_.student),
            )
            for _ in data
        ]
