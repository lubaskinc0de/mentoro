from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Annotated
from uuid import uuid4

from pydantic import BaseModel, Field, StringConstraints
from typing_extensions import Doc

from crudik.adapters.token_encoder import AccessTokenEncoder
from crudik.application.access_token.gateway import AccessTokenGateway
from crudik.application.data_model.token_data import TokenResponse
from crudik.application.student.gateway import StudentGateway
from crudik.application.uow import UoW
from crudik.models.student import Student


class SignUpStudentRequest(BaseModel):
    full_name: Annotated[str, Doc("Student full name")] = Field(min_length=2, max_length=120)
    interests: Annotated[
        list[Annotated[str, StringConstraints(min_length=2, max_length=30)]], Doc("Student interesrs"),
    ] = Field(min_length=1, max_length=100)


@dataclass(frozen=True, slots=True)
class SignUpStudent:
    uow: UoW
    encryptor: AccessTokenEncoder
    access_token_gateway: AccessTokenGateway
    student_gateway: StudentGateway

    async def execute(self, request: SignUpStudentRequest) -> TokenResponse:
        student_id = uuid4()
        student = Student(
            id=student_id,
            full_name=request.full_name,
            created_at=datetime.now(tz=UTC),
            interests=request.interests,
        )
        self.uow.add(student)

        encoded_access_token = self.encryptor.encrypt(student_id)
        await self.uow.commit()

        return TokenResponse(access_token=encoded_access_token)
