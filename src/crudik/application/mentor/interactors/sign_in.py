from dataclasses import dataclass

from pydantic import BaseModel, Field

from crudik.adapters.idp import UnauthorizedError
from crudik.adapters.token_encoder import TokenEncoder
from crudik.application.access_token.gateway import AccessTokenGateway
from crudik.application.data_model.token_data import TokenResponse
from crudik.application.mentor.gateway import MentorGateway
from crudik.application.uow import UoW


class SignInMentorRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=120, description="Mentor full name")


@dataclass(frozen=True, slots=True)
class SignInMentor:
    uow: UoW
    encryptor: TokenEncoder
    access_token_gateway: AccessTokenGateway
    mentor_gateway: MentorGateway

    async def execute(self, request: SignInMentorRequest) -> TokenResponse:
        mentor = await self.mentor_gateway.get_by_name(request.full_name)
        if mentor is None:
            raise UnauthorizedError

        encoded_access_token = self.encryptor.encrypt(mentor.id)
        await self.uow.commit()

        return TokenResponse(access_token=encoded_access_token)
