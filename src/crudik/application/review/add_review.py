from dataclasses import dataclass
from typing import Annotated
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, StringConstraints

from crudik.adapters.idp import TokenStudentIdProvider, UnauthorizedError
from crudik.application.data_model.review import ReviewData, convert_review_to_dto
from crudik.application.mentor.errors import MentorDoesNotExistsError
from crudik.application.mentor.gateway import MentorGateway
from crudik.application.student.gateway import StudentGateway
from crudik.application.uow import UoW
from crudik.models.mentor import MentorReview


class ReviewCreateData(BaseModel):
    mentor_id: UUID
    student_id: UUID
    text: Annotated[str, StringConstraints(min_length=10, max_length=150)] = Field(description="Review text")
    rate: int = Field(description="Mentor review rate", ge=1, le=5)


@dataclass(slots=True, frozen=True)
class AddReview:
    gateway: MentorGateway
    student_gateway: StudentGateway
    idp: TokenStudentIdProvider
    uow: UoW

    async def execute(self, data: ReviewCreateData) -> ReviewData:
        student = await self.student_gateway.get_by_id(await self.idp.get_student_id())
        if student is None:
            raise UnauthorizedError

        mentor = await self.gateway.get_by_id(data.mentor_id)

        if mentor is None:
            raise MentorDoesNotExistsError

        review = MentorReview(
            review_id=uuid4(),
            student_id=student.id,
            mentor_id=mentor.id,
            text=data.text,
            rate=data.rate,
        )
        self.uow.add(review)
        await self.uow.commit()

        return convert_review_to_dto(review)
