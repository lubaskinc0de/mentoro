from dataclasses import dataclass
from io import BufferedReader
from typing import Generic, TypeVar
from uuid import UUID

from aiohttp import ClientResponse, ClientSession

from crudik.application.data_model.mentor import MentorData
from crudik.application.data_model.mentoring_request import MentoringRequestData
from crudik.application.data_model.review import ReviewData, ReviewFullData
from crudik.application.data_model.student import StudentData
from crudik.application.data_model.token_data import TokenResponse
from crudik.application.mentor.attach_avatar import MentorAvatarData
from crudik.application.mentor.sign_in import SignInMentorRequest
from crudik.application.mentor.sign_up import SignUpMentorRequest
from crudik.application.mentor.update import UpdateMentorRequest
from crudik.application.mentoring_request.send import SendMentoringByUserRequest
from crudik.application.mentoring_request.verdict import VerdictMentoringRequestQuery
from crudik.application.review.add_review import ReviewCreateData
from crudik.application.student.attach_avatar import StudentAvatarData
from crudik.application.student.sign_in import SignInStudentRequest
from crudik.application.student.sign_up import SignUpStudentRequest
from crudik.application.student.swipe_mentor import SwipeMentorRequest
from crudik.application.student.update import UpdateStudentRequest

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

        if data is None:
            return Response(status_code=response.status)

        return Response(
            model=model.model_validate(data),  # type: ignore
            status_code=response.status,
        )

    async def sign_up_student(self, schema: SignUpStudentRequest) -> Response[TokenResponse]:
        async with self._session.post(
            "/student/sign_up",
            json=schema.model_dump(),
        ) as response:
            return await self._parse_response(response, TokenResponse)

    async def sign_in_student(self, schema: SignInStudentRequest) -> Response[TokenResponse]:
        async with self._session.post(
            "/student/sign_in",
            json=schema.model_dump(),
        ) as response:
            return await self._parse_response(response, TokenResponse)

    async def student_get_me(self, token: str) -> Response[StudentData]:
        async with self._session.get("/student/me", headers={"Authorization": f"Bearer {token}"}) as response:
            return await self._parse_response(response, StudentData)

    async def student_get_by_id(self, mentor_token: str, student_id: UUID) -> Response[StudentData]:
        async with self._session.get(
            f"/student/{student_id}",
            headers={"Authorization": f"Bearer {mentor_token}"},
        ) as response:
            return await self._parse_response(response, StudentData)

    async def student_update_avatar(self, token: str, file: BufferedReader) -> Response[StudentAvatarData]:
        async with self._session.put(
            "/student/attach",
            headers={"Authorization": f"Bearer {token}"},
            data={"file": file},
        ) as response:
            return await self._parse_response(response, StudentAvatarData)

    async def student_update(self, token: str, schema: UpdateStudentRequest) -> Response[None]:
        async with self._session.patch(
            "/student/",
            headers={"Authorization": f"Bearer {token}"},
            json=schema.model_dump(),
        ) as response:
            return await self._parse_response(response, None)

    async def sign_up_mentor(self, schema: SignUpMentorRequest) -> Response[TokenResponse]:
        async with self._session.post("/mentor/sign_up/", json=schema.model_dump()) as response:
            return await self._parse_response(response, TokenResponse)

    async def sign_in_mentor(self, schema: SignInMentorRequest) -> Response[TokenResponse]:
        async with self._session.post("/mentor/sign_in", json=schema.model_dump()) as response:
            return await self._parse_response(response, TokenResponse)

    async def read_mentor(self, token: str) -> Response[MentorData]:
        async with self._session.get("/mentor/me", headers={"Authorization": f"Bearer {token}"}) as response:
            return await self._parse_response(response, MentorData)

    async def read_mentor_by_id(self, student_token: str, mentor_id: UUID) -> Response[MentorData]:
        async with self._session.get(
            f"/mentor/{mentor_id}",
            headers={"Authorization": f"Bearer {student_token}"},
        ) as response:
            return await self._parse_response(response, MentorData)

    async def find_student(self, token: str) -> Response[list[MentorData]]:
        async with self._session.get("/student/find", headers={"Authorization": f"Bearer {token}"}) as response:
            return Response(
                status_code=response.status, model=[MentorData.model_validate(x) for x in await response.json()]
            )

    async def mentor_update_avatar(self, token: str, file: BufferedReader) -> Response[MentorAvatarData]:
        async with self._session.put(
            "/mentor/attach",
            headers={"Authorization": f"Bearer {token}"},
            data={"file": file},
        ) as response:
            return await self._parse_response(response, MentorAvatarData)

    async def swipe_mentor(self, student_token: str, schema: SwipeMentorRequest) -> Response[None]:
        async with self._session.post(
            "/student/swipe_mentor",
            json=schema.model_dump(mode="json"),
            headers={"Authorization": f"Bearer {student_token}"},
        ) as response:
            return await self._parse_response(response, None)

    async def read_favorites_mentors(self, student_token: str) -> Response[list[MentorData]]:
        async with self._session.get(
            "/student/favorite",
            headers={"Authorization": f"Bearer {student_token}"},
        ) as response:
            if response.status >= 400:
                return Response(status_code=response.status)
            data = await response.json()
            return Response(
                status_code=response.status,
                model=[MentorData.model_validate(_) for _ in data],
            )

    async def delete_favorites_mentors(self, student_token: str, mentor_id: UUID) -> Response[None]:
        async with self._session.delete(
            f"/student/favorite/{mentor_id}",
            headers={"Authorization": f"Bearer {student_token}"},
        ) as response:
            return await self._parse_response(response, None)

    async def update_mentor(self, token: str, schema: UpdateMentorRequest) -> Response[None]:
        async with self._session.put(
            "/mentor/",
            headers={"Authorization": f"Bearer {token}"},
            json=schema.model_dump(),
        ) as response:
            return await self._parse_response(response, None)

    async def send_mentoring(self, schema: SendMentoringByUserRequest, token: str) -> Response[None]:
        async with self._session.post(
            "/student/request",
            headers={"Authorization": f"Bearer {token}"},
            json=schema.model_dump(mode="json"),
        ) as response:
            return await self._parse_response(response, None)

    async def read_student_requests(self, token: str) -> Response[list[MentoringRequestData]]:
        async with self._session.get(
            "/student/request",
            headers={"Authorization": f"Bearer {token}"},
        ) as response:
            if response.status >= 400:
                return Response(status_code=response.status)

            data = await response.json()
            return Response(
                status_code=response.status,
                model=[MentoringRequestData.model_validate(_) for _ in data],
            )

    async def add_review(self, token: str, schema: ReviewCreateData) -> Response[ReviewData]:
        async with self._session.post(
            "/review/",
            headers={"Authorization": f"Bearer {token}"},
            json=schema.model_dump(mode="json"),
        ) as response:
            return await self._parse_response(response, ReviewData)

    async def delete_review(self, token: str, review_id: UUID) -> Response[None]:
        async with self._session.delete(
            f"/review/{review_id}",
            headers={"Authorization": f"Bearer {token}"},
        ) as response:
            return await self._parse_response(response, None)

    async def read_reviews(self, token: str, mentor_id: UUID) -> Response[list[ReviewFullData]]:
        async with self._session.get(
            f"/review/{mentor_id}",
            headers={"Authorization": f"Bearer {token}"},
        ) as response:
            if response.status >= 400:
                return Response(status_code=response.status)

            data = await response.json()
            return Response(
                status_code=response.status,
                model=[ReviewFullData.model_validate(_) for _ in data],
            )

    async def verdict_mentor(self, token: str, schema: VerdictMentoringRequestQuery) -> Response[None]:
        async with self._session.post(
            "/mentor/request/verdict",
            headers={"Authorization": f"Bearer {token}"},
            json=schema.model_dump(mode="json"),
        ) as response:
            return await self._parse_response(response, None)
