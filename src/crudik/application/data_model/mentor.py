from uuid import UUID

from adaptix.conversion import get_converter
from pydantic import BaseModel

from crudik.models.mentor import Mentor


class MentorData(BaseModel):
    id: UUID
    full_name: str
    contacts: list[str]
    description: str | None = None
    photo_url: str | None = None


convert_mentor_model_to_dto = get_converter(Mentor, MentorData)
