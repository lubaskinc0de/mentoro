from uuid import UUID

from adaptix.conversion import get_converter
from pydantic import BaseModel

from crudik.models.student import Student


class StudentData(BaseModel):
    id: UUID
    full_name: str
    age: int | None = None
    interests: list[str]
    avatar_url: str | None = None


convert_student_model_to_dto = get_converter(Student, StudentData)
