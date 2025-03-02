from uuid import UUID

from adaptix.conversion import coercer, get_converter
from pydantic import BaseModel, Field

from crudik.models.mentor import Mentor, MentorSkill


class MentorData(BaseModel):
    id: UUID = Field(description="Id mentor")
    full_name: str = Field(description="Mentor full name")
    contacts: list[str] = Field(description="Mentor contatcs")
    skills: list[str] = Field(description="Mentor skills")
    description: str | None = Field(description="Mentor description", default=None)
    photo_url: str | None = Field(description="Mentor photo url", default=None)


convert_mentor_to_dto = get_converter(Mentor, MentorData, recipe=[coercer(MentorSkill, str, lambda x: x.text)])
