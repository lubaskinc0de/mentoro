from collections.abc import Sequence
from uuid import UUID

from adaptix.conversion import coercer, get_converter
from pydantic import BaseModel

from crudik.application.data_model.mentor import MentorData
from crudik.application.data_model.student import StudentData
from crudik.models.mentor import MentorContact, MentorReview, MentorSkill


class ReviewData(BaseModel):
    mentor_id: UUID
    student_id: UUID
    text: str
    rate: int


class ReviewFullData(BaseModel):
    mentor: MentorData
    student: StudentData
    text: str
    rate: int


convert_review_to_dto = get_converter(MentorReview, ReviewData)
convert_full_reviews_to_dto = get_converter(
    Sequence[MentorReview],
    list[ReviewFullData],
    recipe=[
        coercer(MentorSkill, str, lambda x: x.text),
        coercer(MentorContact, str, lambda x: x.url),
    ],
)
convert_full_review_to_dto = get_converter(
    MentorReview,
    ReviewFullData,
    recipe=[
        coercer(MentorSkill, str, lambda x: x.text),
        coercer(MentorContact, str, lambda x: x.url),
    ],
)
