from dataclasses import dataclass
from typing import Annotated
from uuid import uuid4

from pydantic import BaseModel, Field, StringConstraints

from crudik.adapters.idp import TokenMentorIdProvider, UnauthorizedError
from crudik.application.common.uow import UoW
from crudik.application.data_model.mentor import MentorContactModel
from crudik.application.gateway.mentor_contact import MentorContactGateway
from crudik.application.gateway.mentor_gateway import MentorGateway
from crudik.application.gateway.mentor_skill import MentorSkillGateway
from crudik.models.mentor import MentorContact, MentorSkill


class UpdateMentorRequest(BaseModel):
    description: str | None = Field(min_length=10, max_length=2000, description="Новое описание ментора")
    contacts: list[MentorContactModel] = Field(
        min_length=1,
        max_length=10,
        description="Новые контакты ментора",
    )
    skills: list[Annotated[str, StringConstraints(min_length=2, max_length=30)]] = Field(
        min_length=1,
        max_length=100,
        description="Новые скиллы ментора",
    )


@dataclass(frozen=True, slots=True)
class UpdateMentor:
    uow: UoW
    gateway: MentorGateway
    skill_gateway: MentorSkillGateway
    contact_gateway: MentorContactGateway
    id_provider: TokenMentorIdProvider

    async def execute(self, request: UpdateMentorRequest) -> None:
        mentor_id = await self.id_provider.get_mentor_id()
        mentor = await self.gateway.get_by_id(mentor_id)
        if mentor is None:
            raise UnauthorizedError

        mentor.description = request.description

        await self.skill_gateway.delete_by_mentor_id(mentor.id)
        skills = [
            MentorSkill(id=uuid4(), mentor_id=mentor_id, text=skill)
            for skill in list({key: None for key in request.skills}.keys())
        ]
        self.uow.add_all(skills)

        await self.contact_gateway.delete_by_mentor_id(mentor.id)
        contacts = [
            MentorContact(id=uuid4(), url=contact.url, mentor_id=mentor_id, social_network=contact.social_network)
            for contact in list({cont.url: cont for cont in request.contacts}.values())
        ]

        self.uow.add_all(contacts)

        await self.uow.commit()
