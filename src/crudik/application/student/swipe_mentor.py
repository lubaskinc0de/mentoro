import datetime
import logging
from dataclasses import dataclass
from uuid import UUID, uuid4

from pydantic import BaseModel

from crudik.adapters.idp import TokenStudentIdProvider, UnauthorizedError
from crudik.application.common.uow import UoW
from crudik.application.errors.mentor_errors import MentorDoesNotExistsError
from crudik.application.gateway.mentor_gateway import MentorGateway
from crudik.application.gateway.student_gateway import StudentGateway
from crudik.models.mentor import MatchHistory
from crudik.models.mentoring_request import MentoringRequest, MentoringRequestType
from crudik.models.swiped_mentor import SwipedMentor, SwipedMentorType


class SwipeMentorRequest(BaseModel):
    mentor_id: UUID
    type: SwipedMentorType


@dataclass(frozen=True, slots=True)
class SwipeMentor:
    uow: UoW
    mentor_gateway: MentorGateway
    student_gateway: StudentGateway
    id_provider: TokenStudentIdProvider

    async def execute(self, request: SwipeMentorRequest) -> None:
        student_id = await self.id_provider.get_student_id()
        student = await self.student_gateway.get_by_id(student_id)

        if student is None:
            raise UnauthorizedError

        mentor = await self.mentor_gateway.get_by_id(request.mentor_id)

        if mentor is None:
            raise MentorDoesNotExistsError

        if await self.mentor_gateway.exists_in_history(student.id, mentor.id):
            logging.info("Swipe already exists")
            return

        swiped_mentor = SwipedMentor(
            id=uuid4(),
            mentor_id=mentor.id,
            student_id=student.id,
            type=request.type,
            created_at=datetime.datetime.now(tz=datetime.UTC),
        )
        self.uow.add(swiped_mentor)

        if request.type == SwipedMentorType.LIKE:
            mentoring_request = MentoringRequest(
                id=uuid4(),
                mentor_id=mentor.id,
                student_id=student.id,
                type=MentoringRequestType.REVIEW,
                created_at=datetime.datetime.now(tz=datetime.UTC),
            )
            self.uow.add(mentoring_request)

        logging.info("Adding %s to history", mentor.id)
        history_record = MatchHistory(
            student_id=student.id,
            mentor_id=mentor.id,
        )
        self.uow.add(history_record)
        await self.uow.commit()
