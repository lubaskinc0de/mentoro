from dataclasses import dataclass
from enum import Enum
from uuid import UUID

from crudik.adapters.idp import TokenStudentIdProvider, UnauthorizedError
from crudik.application.mentoring_request.errors import (
    MentoringRequestCannotBeUpdatedError,
    MentoringRequestNotFoundError,
)
from crudik.application.mentoring_request.gateway import MentoringRequestGateway
from crudik.application.student.gateway import StudentGateway
from crudik.application.uow import UoW
from crudik.models.mentoring_request import MentoringRequestType


class VerdictMentoringRequestType(Enum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"


@dataclass(frozen=True, slots=True)
class VerdictMentoringRequestQuery:
    mentoring_request_id: UUID
    type: VerdictMentoringRequestType


@dataclass(frozen=True, slots=True)
class VerdictMentoringRequest:
    uow: UoW
    student_gateway: StudentGateway
    gateway: MentoringRequestGateway
    id_provider: TokenStudentIdProvider

    async def execute(self, request: VerdictMentoringRequestQuery) -> None:
        student_id = await self.id_provider.get_student_id()
        student = await self.student_gateway.get_by_id(student_id)
        if student is None:
            raise UnauthorizedError

        mentoring_request = await self.gateway.get_by_id(student.id)
        if mentoring_request is None:
            raise MentoringRequestNotFoundError

        if mentoring_request.type != MentoringRequestType.REVIEW:
            raise MentoringRequestCannotBeUpdatedError

        mentoring_request.type = MentoringRequestType(request.type.value)

        await self.uow.commit()
