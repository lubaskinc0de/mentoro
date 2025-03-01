from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Annotated
from uuid import uuid4

from pydantic import BaseModel, Field, StringConstraints

from crudik.adapters.token_encoder import TokenEncoder
from crudik.application.access_token.gateway import AccessTokenGateway
from crudik.application.data_model.token_data import TokenResponse
from crudik.application.mentor.gateway import MentorGateway
from crudik.application.uow import UoW
from crudik.models.mentor import Mentor, MentorSkill


class SignUpMentorRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=120, description="Mentor full name")
    age: int | None = Field(ge=0, le=120, default=None, description="Mentor age")
    descriptiion: str | None = Field(min_length=10, max_length=2000, default=None, description="Mentor description")

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
            description=request.descriptiion,
            contacts=request.contacts,
            created_at=datetime.now(tz=UTC),
        )

        skills = [MentorSkill(id=uuid4(), mentor_id=mentor_id, text=skill) for skill in request.skills]

        self.uow.add(mentor)
        self.uow.add_all(skills)

        encoded_access_token = self.encryptor.encrypt(mentor_id)
        await self.uow.commit()

        return TokenResponse(access_token=encoded_access_token)
