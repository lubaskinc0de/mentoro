from uuid import UUID

from adaptix.conversion import get_converter
from pydantic import BaseModel

from crudik.models.mentor import Mentor


class MentorData(BaseModel):
    id: UUID
    full_name: str
    description: str | None = None
    photo_url: str | None = None
    contacts: list[str]


convert_mentor_to_dto = get_converter(Mentor, MentorData)
