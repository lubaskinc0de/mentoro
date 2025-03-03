from dataclasses import dataclass
from uuid import UUID

from crudik.adapters.idp import TokenStudentIdProvider, UnauthorizedError
from crudik.application.data_model.review import ReviewFullData, convert_full_reviews_to_dto
from crudik.application.errors.mentor_errors import MentorDoesNotExistsError
from crudik.application.gateway.mentor_gateway import MentorGateway
from crudik.application.gateway.review_gateway import ReviewGateway
from crudik.application.gateway.student_gateway import StudentGateway


@dataclass(slots=True, frozen=True)
class ReadMentorReviewsByStudent:
    gateway: MentorGateway
    student_gateway: StudentGateway
    idp: TokenStudentIdProvider
    review_gateway: ReviewGateway
    mentor_gateway: MentorGateway

    async def execute(self, mentor_id: UUID) -> list[ReviewFullData]:
        student = await self.student_gateway.get_by_id(await self.idp.get_student_id())
        if student is None:
            raise UnauthorizedError

        mentor = await self.mentor_gateway.get_by_id(mentor_id)
        if mentor is None:
            raise MentorDoesNotExistsError

        reviews: list[ReviewFullData] = convert_full_reviews_to_dto(
            await self.review_gateway.get_mentor_reviews(mentor_id)
        )
        return reviews
