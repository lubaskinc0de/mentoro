import logging
from dataclasses import dataclass
from uuid import UUID

from fastapi import Request
from jwt.exceptions import PyJWTError

from crudik.adapters.token_encoder import TokenEncoder
from crudik.application.errors.common import ApplicationError

TOKEN_TYPE = "Bearer"  # noqa: S105
BEARER_SECTIONS = 2
AUTH_HEADER = "Authorization"


class UnauthorizedError(ApplicationError): ...


@dataclass(slots=True, frozen=True)
class TokenBearerParser:
    request: Request
    encoder: TokenEncoder

    def authorize_request_by_token(self) -> UUID:
        authorization_header = self.request.headers.get(AUTH_HEADER)

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
            logging.warning("Unauthorized due to %s", err.__class__.__qualname__)
            raise UnauthorizedError from err


class TokenStudentIdProvider:
    def __init__(self, parser: TokenBearerParser) -> None:
        self.parser = parser
        self._student_id: UUID | None = None

    async def _authorize_request(self) -> UUID:
        self._student_id = self.parser.authorize_request_by_token()
        return self._student_id

    async def get_student_id(self) -> UUID:
        if self._student_id:
            return self._student_id
        return await self._authorize_request()


class TokenMentorIdProvider:
    def __init__(self, parser: TokenBearerParser) -> None:
        self.parser = parser
        self._mentor_id: UUID | None = None

    async def _authorize_request(self) -> UUID:
        self._mentor_id = self.parser.authorize_request_by_token()
        return self._mentor_id

    async def get_mentor_id(self) -> UUID:
        if self._mentor_id:
            return self._mentor_id
        return await self._authorize_request()
