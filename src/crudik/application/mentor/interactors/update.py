from dataclasses import dataclass
from typing import Annotated
from uuid import uuid4

from pydantic import BaseModel, Field, StringConstraints

from crudik.adapters.idp import TokenMentorIdProvider
from crudik.application.mentor.gateway import MentorGateway
from crudik.application.mentor_skill.gateway import MentorSkillGateway
from crudik.application.student.errors import StudentDoesNotExistsError
from crudik.application.uow import UoW
from crudik.models.mentor import MentorSkill


class UpdateMentorRequest(BaseModel):
    age: int = Field(ge=0, le=120, description="Mentor age")
    description: str = Field(min_length=10, max_length=2000, description="Mentor description")
    contacts: list[Annotated[str, StringConstraints(min_length=2, max_length=40)]] = Field(
        min_length=1,
        max_length=10,
        description="Mentor contacts",
    )
    skills: list[Annotated[str, StringConstraints(min_length=2, max_length=30)]] = Field(
        min_length=1,
        max_length=100,
        description="Mentor skills",
    )


@dataclass(frozen=True, slots=True)
class UpdateMentor:
    uow: UoW
    gateway: MentorGateway
    skill_gateway: MentorSkillGateway
    id_provider: TokenMentorIdProvider

    async def execute(self, request: UpdateMentorRequest) -> None:
        mentor_id = await self.id_provider.get_mentor_id()
        mentor = await self.gateway.get_by_id(mentor_id)
        if mentor is None:
            raise StudentDoesNotExistsError

        mentor.age = request.age
        mentor.description = request.description
        mentor.contacts = request.contacts

        await self.skill_gateway.delete_by_mentor_id(mentor.id)
        skills = [MentorSkill(id=uuid4(), mentor_id=mentor_id, text=skill) for skill in request.skills]

        self.uow.add_all(skills)

        await self.uow.commit()
