from dataclasses import dataclass
from uuid import UUID

from crudik.adapters.idp import TokenStudentIdProvider, UnauthorizedError
from crudik.application.common.errors import AccessDeniedError
from crudik.application.mentor.gateway import MentorGateway
from crudik.application.review.common import ReviewGateway
from crudik.application.review.errors import ReviewDoesNotExistsError
from crudik.application.student.gateway import StudentGateway
from crudik.application.uow import UoW


@dataclass(slots=True, frozen=True)
class DeleteReview:
    gateway: MentorGateway
    student_gateway: StudentGateway
    idp: TokenStudentIdProvider
    uow: UoW
    review_gateway: ReviewGateway

    async def execute(self, review_id: UUID) -> None:
        student = await self.student_gateway.get_by_id(await self.idp.get_student_id())
        if student is None:
            raise UnauthorizedError

        review = await self.review_gateway.get_review(review_id)
        if review is None:
            raise ReviewDoesNotExistsError
        if review.student_id != student.id:
            raise AccessDeniedError

        await self.uow.delete(review)
        await self.uow.commit()
