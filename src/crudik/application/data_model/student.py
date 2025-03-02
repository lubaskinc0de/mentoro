from uuid import UUID

from adaptix.conversion import get_converter
from pydantic import BaseModel, Field

from crudik.models.student import Student


class StudentData(BaseModel):
    id: UUID = Field(description="Идентификатор студента")
    full_name: str = Field(description="Полное имя студента")
    interests: list[str] = Field(description="Интересы студента")
    age: int | None = Field(default=None, description="Возраст студента")
    avatar_url: str | None = Field(default=None, description="Ссылка на аватарку студента")
    description: str | None = Field(default=None, description="Описание студента")


convert_student_model_to_dto = get_converter(Student, StudentData)
