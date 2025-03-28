from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Annotated
from uuid import uuid4

from pydantic import BaseModel, Field, StringConstraints

from crudik.adapters.token_encoder import TokenEncoder
from crudik.application.common.uow import UoW
from crudik.application.data_model.mentor import MentorContactModel
from crudik.application.data_model.token_data import TokenResponse
from crudik.application.gateway.mentor_gateway import MentorGateway
from crudik.application.gateway.token_gateway import AccessTokenGateway
from crudik.models.mentor import Mentor, MentorContact, MentorSkill


class SignUpMentorRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=120, description="Полное имя ментора")
    description: str | None = Field(min_length=1, max_length=2000, default=None, description="Описание ментора")

    contacts: list[MentorContactModel] = Field(
        min_length=1,
        max_length=10,
        description="Контакты ментора",
    )
    skills: list[Annotated[str, StringConstraints(min_length=2, max_length=30)]] = Field(
        min_length=1,
        max_length=100,
        description="Скиллы ментора",
    )


@dataclass(frozen=True, slots=True)
class SignUpMentor:
    uow: UoW
    encryptor: TokenEncoder
    access_token_gateway: AccessTokenGateway
    mentor_gateway: MentorGateway

    async def execute(self, request: SignUpMentorRequest) -> TokenResponse:
        mentor_id = uuid4()
        mentor = Mentor(
            id=mentor_id,
            full_name=request.full_name,
            description=request.description,
            created_at=datetime.now(tz=UTC),
        )

        skills = [
            MentorSkill(id=uuid4(), mentor_id=mentor_id, text=skill)
            for skill in list({key: None for key in request.skills}.keys())
        ]
        contacts = [
            MentorContact(id=uuid4(), url=contact.url, mentor_id=mentor_id, social_network=contact.social_network)
            for contact in list({cont.url: cont for cont in request.contacts}.values())
        ]

        self.uow.add(mentor)
        self.uow.add_all(skills)
        self.uow.add_all(contacts)

        encoded_access_token = self.encryptor.encrypt(mentor_id)
        await self.uow.commit()

        return TokenResponse(access_token=encoded_access_token, id=mentor_id)
