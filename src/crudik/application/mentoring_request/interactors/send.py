import datetime
from dataclasses import dataclass
from uuid import UUID, uuid4

from pydantic import BaseModel

from crudik.adapters.idp import TokenStudentIdProvider, UnauthorizedError
from crudik.application.mentor.errors import MentorDoesNotExistsError
from crudik.application.mentor.gateway import MentorGateway
from crudik.application.student.gateway import StudentGateway
from crudik.application.uow import UoW
from crudik.models.mentoring_request import MentoringRequest, MentoringRequestType


class SendMentoringByUserRequest(BaseModel):
    mentor_id: UUID


@dataclass(frozen=True, slots=True)
class SendMentoringByStudent:
    uow: UoW
    mentor_gateway: MentorGateway
    student_gateway: StudentGateway
    id_provider: TokenStudentIdProvider

    async def execute(self, request: SendMentoringByUserRequest) -> None:
        student_id = await self.id_provider.get_student_id()
        student = await self.student_gateway.get_by_id(student_id)

        if student is None:
            raise UnauthorizedError

        mentor = await self.mentor_gateway.get_by_id(request.mentor_id)

        if mentor is None:
            raise MentorDoesNotExistsError

        mentoring_request = MentoringRequest(
            id=uuid4(),
            mentor_id=mentor.id,
            student_id=student.id,
            type=MentoringRequestType.REVIEW,
            created_at=datetime.datetime.now(tz=datetime.UTC),
        )
        self.uow.add(mentoring_request)

        await self.uow.commit()
