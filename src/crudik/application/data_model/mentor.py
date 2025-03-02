from collections.abc import Sequence
from typing import Annotated
from uuid import UUID

from adaptix.conversion import coercer, get_converter
from pydantic import BaseModel, Field, StringConstraints

from crudik.models.mentor import Mentor, MentorContact, MentorSkill


class MentorContactModel(BaseModel):
    url: Annotated[str, StringConstraints(min_length=2, max_length=40)] = Field(description="Ссылка для связи")
    social_network: Annotated[str, StringConstraints(min_length=2, max_length=40)] = Field(
        description="Социальная сеть",
    )


class MentorData(BaseModel):
    id: UUID = Field(description="Идентификатор ментор")
    full_name: str = Field(description="Полное имя ментора")
    contacts: list[MentorContactModel] = Field(description="Контакты ментора")
    skills: list[str] = Field(description="Скиллы ментора")
    description: str | None = Field(default=None, description="Описание ментора")
    photo_url: str | None = Field(default=None, description="Ссылка на аватарку ментора")


convert_mentors_to_dto = get_converter(
    Sequence[Mentor],
    list[MentorData],
    recipe=[
        coercer(MentorSkill, str, lambda x: x.text),
        coercer(MentorContact, str, lambda x: x.url),
    ],
)

convert_mentor_to_dto = get_converter(
    Mentor,
    MentorData,
    recipe=[
        coercer(MentorSkill, str, lambda x: x.text),
        coercer(MentorContact, str, lambda x: x.url),
    ],
)
