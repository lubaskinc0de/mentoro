from uuid import UUID

from adaptix.conversion import get_converter
from pydantic import BaseModel, Field

from crudik.models.mentor import Mentor


class MentorData(BaseModel):
    id: UUID = Field(description="Id mentor")
    full_name: str = Field(description="Mentor full name")
    contacts: list[str] = Field(description="Mentor contatcs")
    description: str | None = Field(description="Mentor description", default=None)
    photo_url: str | None = Field(description="Mentor photo url", default=None)


convert_mentor_to_dto = get_converter(Mentor, MentorData)
