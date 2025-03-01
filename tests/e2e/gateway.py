from dataclasses import dataclass
from typing import Generic, TypeVar

from aiohttp import ClientResponse, ClientSession

from crudik.application.data_model.student import StudentData
from crudik.application.data_model.token_data import TokenResponse
from crudik.application.student.interactors.sign_in import SignInStudentRequest
from crudik.application.student.interactors.sign_up import SignUpStudentRequest

ModelT = TypeVar("ModelT")


@dataclass
class Response(Generic[ModelT]):
    status_code: int
    model: ModelT | None = None


class TestApiGateway:
    def __init__(self, session: ClientSession) -> None:
        self._session = session

    async def _parse_response(self, response: ClientResponse, model: type[ModelT]) -> Response[ModelT]:
        if response.status >= 400:
            return Response(status_code=response.status)

        data = await response.json()

        return Response(
            model=model.model_validate(data),  # type: ignore
            status_code=response.status,
        )

    async def sign_up_client(self, schema: SignUpStudentRequest) -> Response[TokenResponse]:
        async with self._session.post(
            "/student/sign_up",
            json=schema.model_dump(),
        ) as response:
            return await self._parse_response(response, TokenResponse)

    async def sign_in_client(self, schema: SignInStudentRequest) -> Response[TokenResponse]:
        async with self._session.post(
            "/student/sign_in",
            json=schema.model_dump(),
        ) as response:
            return await self._parse_response(response, TokenResponse)

    async def student_get_me(self, token: str) -> Response[StudentData]:
        async with self._session.get("/student/me", headers={"Authorization": f"Bearer {token}"}) as response:
            return await self._parse_response(response, StudentData)
