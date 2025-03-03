from dataclasses import dataclass

from crudik.adapters.idp import TokenStudentIdProvider, UnauthorizedError
from crudik.application.data_model.mentor import MentorData, convert_mentor_to_dto
from crudik.application.gateway.student_gateway import StudentGateway
from crudik.application.gateway.swiped_gateway import SwipedMentorGateway
from crudik.models.swiped_mentor import SwipedMentorType


@dataclass(frozen=True, slots=True)
class ReadFavoritesMentors:
    swiped_mentors_gateway: SwipedMentorGateway
    id_provider: TokenStudentIdProvider
    student_gateway: StudentGateway

    async def execute(self) -> list[MentorData]:
        student_id = await self.id_provider.get_student_id()
        student = await self.student_gateway.get_by_id(student_id)
        if student is None:
            raise UnauthorizedError

        swiped_mentors = await self.swiped_mentors_gateway.get_all(
            student_id=student.id,
            swiped_mentor_type=SwipedMentorType.FAVORITES,
        )
        data = [convert_mentor_to_dto(swiped_mentor.mentor) for swiped_mentor in swiped_mentors]

        for mentor in data:
            mentor.contacts = []

        return data
