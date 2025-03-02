import logging
from dataclasses import dataclass
from uuid import UUID

from crudik.adapters.idp import TokenStudentIdProvider, UnauthorizedError
from crudik.application.mentor.errors import MentorDoesNotExistsError
from crudik.application.mentor.gateway import MentorGateway
from crudik.application.student.gateway import StudentGateway
from crudik.application.swiped_mentor.errors import SwipedMentorNotFoundError
from crudik.application.swiped_mentor.gateway import SwipedMentorGateway
from crudik.application.uow import UoW


@dataclass(frozen=True, slots=True)
class DeleteFavoritesMentor:
    uow: UoW
    swiped_mentors_gateway: SwipedMentorGateway
    id_provider: TokenStudentIdProvider
    student_gateway: StudentGateway
    mentor_gateway: MentorGateway

    async def execute(self, mentor_id: UUID) -> None:
        student_id = await self.id_provider.get_student_id()
        student = await self.student_gateway.get_by_id(student_id)
        if student is None:
            raise UnauthorizedError

        mentor = await self.mentor_gateway.get_by_id(mentor_id)
        if mentor is None:
            raise MentorDoesNotExistsError

        swiped_mentor = await self.swiped_mentors_gateway.read(
            student_id=student.id,
            mentor_id=mentor.id,
        )
        if swiped_mentor is None:
            raise SwipedMentorNotFoundError

        logging.info("Deleting favorite %s", mentor.full_name)
        await self.swiped_mentors_gateway.delete(swiped_mentor)
        await self.uow.commit()
