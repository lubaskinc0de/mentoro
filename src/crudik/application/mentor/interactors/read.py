from dataclasses import dataclass

from crudik.adapters.idp import TokenMentorIdProvider, UnauthorizedError
from crudik.application.data_model.mentor import MentorData, convert_mentor_to_dto
from crudik.application.mentor.gateway import MentorGateway


@dataclass(slots=True, frozen=True)
class ReadMentor:
    gateway: MentorGateway
    id_provider: TokenMentorIdProvider

    async def execute(self) -> MentorData:
        mentor_id = await self.id_provider.get_mentor_id()
        mentor = await self.gateway.get_by_id(mentor_id)

        if mentor is None:
            raise UnauthorizedError

        return convert_mentor_to_dto(mentor)
