from dataclasses import dataclass
from io import BufferedReader
from typing import Generic, TypeVar

from aiohttp import ClientResponse, ClientSession

from crudik.application.data_model.mentor import MentorData
from crudik.application.data_model.student import StudentData
from crudik.application.data_model.token_data import TokenResponse
from crudik.application.mentor.interactors.sign_in import SignInMentorRequest
from crudik.application.student.interactors.attach_avatar import StudentAvatarData
from crudik.application.student.interactors.sign_in import SignInStudentRequest
from crudik.application.student.interactors.update import UpdateStudentRequest

ModelT = TypeVar("ModelT")


@dataclass
class Response(Generic[ModelT]):
    status_code: int
    model: ModelT | None = None


class TestApiGateway:
    def __init__(self, session: ClientSession) -> None:
        self._session = session

    async def _parse_response(self, response: ClientResponse, model: type[ModelT] | None) -> Response[ModelT]:
        if response.status >= 400:
            return Response(status_code=response.status)

        if model is None:
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

    async def student_update_avatar(self, token: str, file: BufferedReader) -> Response[StudentAvatarData]:
        async with self._session.put(
            "/student/attach",
            headers={"Authorization": f"Bearer {token}"},
            data={"file": file},
        ) as response:
            return await self._parse_response(response, StudentAvatarData)

    async def student_update(self, token: str, schema: UpdateStudentRequest) -> Response[None]:
        async with self._session.put(
            "/student/",
            headers={"Authorization": f"Bearer {token}"},
            json=schema.model_dump(),
        ) as response:
            return await self._parse_response(response, None)
    
    async def sign_up_mentor(self, schema: SignUpMentorRequest) -> Response[TokenResponse]:
        async with self._session.post("/mentor/sign_up", json=schema.model_dump()) as response:
            return await self._parse_response(response, TokenResponse)
        
    async def sign_in_mentor(self, schema: SignInMentorRequest) -> Response[TokenResponse]:
        async with self._session.post("/mentor/sign_in", json=schema.model_dump()) as response:
            return await self._parse_response(response, TokenResponse)
     
    async def read_mentor(self, token: str) -> Response[MentorData]:
        async with self._session.post("/mentor/mr", headers={"Authorization": f"Bearer {token}"}) as response:
            return await self._parse_response(response, MentorData)
