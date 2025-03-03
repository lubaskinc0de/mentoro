from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Annotated
from uuid import uuid4

from pydantic import BaseModel, Field, StringConstraints

from crudik.adapters.token_encoder import TokenEncoder
from crudik.application.common.uow import UoW
from crudik.application.data_model.token_data import TokenResponse
from crudik.application.gateway.student_gateway import StudentGateway
from crudik.application.gateway.token_gateway import AccessTokenGateway
from crudik.models.student import Student


class SignUpStudentRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=120, description="Полное имя студента")
    age: int | None = Field(ge=0, le=120, default=None, description="Возраст студента")
    interests: list[Annotated[str, StringConstraints(min_length=2, max_length=30)]] = Field(
        min_length=1,
        max_length=100,
        description="Интересы студента",
    )
    description: str | None = Field(max_length=150, min_length=2, description="Описание студента", default=None)


@dataclass(frozen=True, slots=True)
class SignUpStudent:
    uow: UoW
    encryptor: TokenEncoder
    access_token_gateway: AccessTokenGateway
    student_gateway: StudentGateway

    async def execute(self, request: SignUpStudentRequest) -> TokenResponse:
        student_id = uuid4()
        student = Student(
            id=student_id,
            full_name=request.full_name,
            created_at=datetime.now(tz=UTC),
            interests=list({key: None for key in request.interests}.keys()),
            age=request.age,
            description=request.description,
        )
        self.uow.add(student)

        encoded_access_token = self.encryptor.encrypt(student_id)
        await self.uow.commit()

        return TokenResponse(access_token=encoded_access_token, id=student_id)
