from dataclasses import dataclass
from enum import Enum
from uuid import UUID

from crudik.adapters.idp import TokenMentorIdProvider, UnauthorizedError
from crudik.application.mentor.gateway import MentorGateway
from crudik.application.mentoring_request.errors import (
    MentoringRequestCannotBeUpdatedError,
    MentoringRequestNotFoundError,
)
from crudik.application.mentoring_request.gateway import MentoringRequestGateway
from crudik.application.uow import UoW
from crudik.models.mentoring_request import MentoringRequestType


class VerdictMentoringRequestType(Enum):
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


@dataclass(frozen=True, slots=True)
class VerdictMentoringRequestQuery:
    mentoring_request_id: UUID
    type: VerdictMentoringRequestType


@dataclass(frozen=True, slots=True)
class VerdictMentoringRequest:
    uow: UoW
    mentor_gateway: MentorGateway
    gateway: MentoringRequestGateway
    id_provider: TokenMentorIdProvider

    async def execute(self, request: VerdictMentoringRequestQuery) -> None:
        mentor_id = await self.id_provider.get_mentor_id()
        mentor = await self.mentor_gateway.get_by_id(mentor_id)
        if mentor is None:
            raise UnauthorizedError

        mentoring_request = await self.gateway.get_by_id(request.mentoring_request_id)
        if mentoring_request is None:
            raise MentoringRequestNotFoundError

        if mentoring_request.type != MentoringRequestType.REVIEW:
            raise MentoringRequestCannotBeUpdatedError

        mentoring_request.type = MentoringRequestType(request.type.value)
        await self.uow.commit()
