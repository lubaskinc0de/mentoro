from uuid import uuid4

from crudik.adapters.test_api_gateway import TestApiGateway
from crudik.application.data_model.mentor import MentorData
from crudik.application.data_model.student import StudentData
from crudik.application.mentoring_request.send import SendMentoringByUserRequest
from crudik.application.mentoring_request.verdict import VerdictMentoringRequestQuery, VerdictMentoringRequestType
from crudik.application.student.sign_up import SignUpStudentRequest
from tests.e2e.conftest import CreatedMentor
from tests.e2e.student.test_request import get_mentor


async def send_mentoring_from_user(api_gateway: TestApiGateway, mentor: MentorData) -> StudentData:
    client = await api_gateway.sign_up_student(
        SignUpStudentRequest(full_name=uuid4().hex, age=32, interests=["skills", "freebsd"])
    )
    assert client.status_code == 200
    assert client.model is not None

    response = await api_gateway.send_mentoring(
        SendMentoringByUserRequest(
            mentor_id=mentor.id,
        ),
        client.model.access_token,
    )

    assert response.status_code == 200

    profile = await api_gateway.student_get_me(token=client.model.access_token)
    assert profile.status_code == 200
    assert profile.model is not None

    return profile.model


async def test_read_requests_mentor(api_gateway: TestApiGateway, created_mentor: CreatedMentor) -> None:
    mentor = await get_mentor(api_gateway, created_mentor)

    first = await send_mentoring_from_user(api_gateway, mentor)
    second = await send_mentoring_from_user(api_gateway, mentor)

    requests = await api_gateway.read_mentors_requests(created_mentor.token.access_token)

    assert requests.status_code == 200
    assert requests.model is not None
    assert len(requests.model) == 2

    await api_gateway.verdict_mentor(
        created_mentor.token.access_token,
        VerdictMentoringRequestQuery(
            mentoring_request_id=requests.model[0].id, type=VerdictMentoringRequestType.ACCEPTED
        ),
    )

    requests = await api_gateway.read_mentors_requests(created_mentor.token.access_token)

    assert requests.status_code == 200
    assert requests.model is not None
    assert len(requests.model) == 2

    assert requests.model[0].student == first
    assert requests.model[1].student == second


async def test_read_requests_mentor_fail_unauthorized(api_gateway: TestApiGateway) -> None:
    requests = await api_gateway.read_mentors_requests("Not access token")

    assert requests.status_code == 401
