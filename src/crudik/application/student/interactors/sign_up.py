from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Annotated
from uuid import uuid4

from argon2 import PasswordHasher
from pydantic import BaseModel, Field
from typing_extensions import Doc

from crudik.adapters.token_encoder import AccessTokenEncoder
from crudik.application.access_token.gateway import AccessTokenGateway
from crudik.application.data_model.token_data import TokenResponse
from crudik.application.student.gateway import StudentGateway
from crudik.application.uow import UoW
from crudik.models.student import Student


class SignUpStudentRequest(BaseModel):
    login: Annotated[str, Doc("Student login")] = Field(min_length=1, max_length=60)
    full_name: Annotated[str, Doc("Student full name")] = Field(min_length=2, max_length=60)
    password: Annotated[str, Doc("Student password")] = Field(min_length=6, max_length=120)


@dataclass(frozen=True, slots=True)
class SignUpStudent:
    uow: UoW
    encryptor: AccessTokenEncoder
    access_token_gateway: AccessTokenGateway
    student_gateway: StudentGateway
    password_hasher: PasswordHasher

    async def execute(self, request: SignUpStudentRequest) -> TokenResponse:
        student_id = uuid4()
        student = Student(
            id=student_id,
            login=request.login,
            full_name=request.full_name,
            password=self.password_hasher.hash(request.password),
            created_at=datetime.now(tz=UTC),
        )
        await self.uow.add(student)

        encoded_access_token = self.encryptor.encrypt(student_id)
        await self.uow.commit()

        return TokenResponse(access_token=encoded_access_token)
