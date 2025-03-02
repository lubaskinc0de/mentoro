from uuid import UUID

from adaptix.conversion import get_converter
from pydantic import BaseModel

from crudik.models.mentor import MentorReview


class ReviewData(BaseModel):
    mentor_id: UUID
    student_id: UUID
    text: str
    rate: int


convert_review_to_dto = get_converter(MentorReview, ReviewData)
