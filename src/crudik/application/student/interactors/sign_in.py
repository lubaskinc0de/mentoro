from dataclasses import dataclass

from pydantic import BaseModel, Field

from crudik.adapters.idp import UnauthorizedError
from crudik.adapters.token_encoder import TokenEncoder
from crudik.application.access_token.gateway import AccessTokenGateway
from crudik.application.data_model.token_data import TokenResponse
from crudik.application.student.gateway import StudentGateway
from crudik.application.uow import UoW


class SignInStudentRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=120, description="Student full name")


@dataclass(frozen=True, slots=True)
class SignInStudent:
    uow: UoW
    encryptor: TokenEncoder
    access_token_gateway: AccessTokenGateway
    student_gateway: StudentGateway

    async def execute(self, request: SignInStudentRequest) -> TokenResponse:
        student = await self.student_gateway.get_by_name(request.full_name)
        if student is None:
            raise UnauthorizedError

        encoded_access_token = self.encryptor.encrypt(student.id)
        await self.uow.commit()

        return TokenResponse(access_token=encoded_access_token)
