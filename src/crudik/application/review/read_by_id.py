from dataclasses import dataclass
from uuid import UUID

from crudik.adapters.idp import TokenStudentIdProvider, UnauthorizedError
from crudik.application.data_model.review import ReviewFullData, convert_full_review_to_dto
from crudik.application.errors.review_errors import ReviewDoesNotExistsError
from crudik.application.gateway.mentor_gateway import MentorGateway
from crudik.application.gateway.review_gateway import ReviewGateway
from crudik.application.gateway.student_gateway import StudentGateway


@dataclass(slots=True, frozen=True)
class ReadReview:
    gateway: MentorGateway
    student_gateway: StudentGateway
    idp: TokenStudentIdProvider
    review_gateway: ReviewGateway

    async def execute(self, review_id: UUID) -> ReviewFullData:
        student = await self.student_gateway.get_by_id(await self.idp.get_student_id())
        if student is None:
            raise UnauthorizedError

        review = await self.review_gateway.get_review(review_id)
        if review is None:
            raise ReviewDoesNotExistsError

        return convert_full_review_to_dto(review)
