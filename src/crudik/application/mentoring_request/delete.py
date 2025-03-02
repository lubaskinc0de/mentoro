from dataclasses import dataclass
from uuid import UUID

from crudik.adapters.idp import TokenStudentIdProvider, UnauthorizedError
from crudik.application.common.uow import UoW
from crudik.application.errors.mentoring_request import MentoringRequestCannotBeDeletedError
from crudik.application.gateway.mentoring_request import MentoringRequestGateway
from crudik.application.gateway.student_gateway import StudentGateway
from crudik.models.mentoring_request import MentoringRequestType


@dataclass(frozen=True, slots=True)
class DeleteMentoringRequestById:
    uow: UoW
    mentoring_request_gateway: MentoringRequestGateway
    student_gateway: StudentGateway
    id_provider: TokenStudentIdProvider

    async def execute(self, mentoring_request_id: UUID) -> None:
        student_id = await self.id_provider.get_student_id()
        student = await self.student_gateway.get_by_id(student_id)

        if student is None:
            raise UnauthorizedError

        mentoring_request = await self.mentoring_request_gateway.get_by_id(mentoring_request_id)

        if mentoring_request is None:
            raise UnauthorizedError

        if mentoring_request.student_id != student.id:
            raise UnauthorizedError

        if mentoring_request.type != MentoringRequestType.REVIEW:
            raise MentoringRequestCannotBeDeletedError

        await self.uow.delete(mentoring_request)

        await self.uow.commit()
