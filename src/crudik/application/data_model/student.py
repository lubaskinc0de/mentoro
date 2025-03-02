from uuid import UUID

from adaptix.conversion import get_converter
from pydantic import BaseModel, Field

from crudik.models.student import Student


class StudentData(BaseModel):
    id: UUID = Field(description="Student id")
    full_name: str = Field(description="Full name")
    age: int | None = Field(description="Age", default=None)
    interests: list[str] = Field(description="Student interests")
    avatar_url: str | None = Field(description="Student avatar url", default=None)
    description: str | None = Field(description="Student description", default=None)


convert_student_model_to_dto = get_converter(Student, StudentData)
