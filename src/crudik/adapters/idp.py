from dataclasses import dataclass
from uuid import UUID

from fastapi import Request
from jwt.exceptions import PyJWTError

from crudik.adapters.token_encoder import TokenEncoder
from crudik.application.common.errors import ApplicationError
from crudik.application.student.gateway import StudentGateway

TOKEN_TYPE = "Bearer"  # noqa: S105
BEARER_SECTIONS = 2


class UnauthorizedError(ApplicationError): ...


@dataclass(slots=True, frozen=True)
class TokenBearerParser:
    request: Request
    encoder: TokenEncoder

    def authorize_request_by_token(self) -> UUID:
        authorization_header = self.request.headers.get("Authorization")

        if authorization_header is None:
            raise UnauthorizedError

        sections = authorization_header.split(" ")
        if len(sections) != BEARER_SECTIONS:
            raise UnauthorizedError

        token_type, token = sections

        if token_type != TOKEN_TYPE:
            raise UnauthorizedError

        try:
            return self.encoder.decrypt(token)
        except PyJWTError as err:
            raise UnauthorizedError from err


class TokenStudentIdProvider:
    def __init__(self, gateway: StudentGateway, parser: TokenBearerParser) -> None:
        self.gateway = gateway
        self.parser = parser
        self._student_id: UUID | None = None

    async def _authorize_request(self) -> UUID:
        self._student_id = self.parser.authorize_request_by_token()
        return self._student_id

    async def get_student_id(self) -> UUID:
        if self._student_id:
            return self._student_id
        return await self._authorize_request()
