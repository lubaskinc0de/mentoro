from uuid import uuid4

from crudik.adapters.test_api_gateway import TestApiGateway
from crudik.application.data_model.mentor import MentorData
from crudik.application.mentor.sign_up import SignUpMentorRequest
from tests.e2e.conftest import CreatedStudent


async def test_success_read(
    mentor: SignUpMentorRequest,
    api_gateway: TestApiGateway,
) -> None:
    sign_up_response = await api_gateway.sign_up_mentor(mentor)
    assert sign_up_response.model is not None

    read_response = await api_gateway.read_mentor(sign_up_response.model.access_token)
    assert read_response.status_code == 200
    assert read_response.model is not None

    expected = MentorData(**mentor.model_dump(), id=read_response.model.id)
    assert expected == read_response.model


async def test_read_by_id(
    mentor: SignUpMentorRequest,
    api_gateway: TestApiGateway,
    created_student: CreatedStudent,
) -> None:
    sign_up_response = await api_gateway.sign_up_mentor(mentor)
    assert sign_up_response.model is not None

    mentor_id = sign_up_response.model.id
    read_response = await api_gateway.read_mentor_by_id(created_student.token.access_token, mentor_id)
    assert read_response.status_code == 200
    assert read_response.model is not None

    expected = MentorData(**mentor.model_dump(), id=read_response.model.id)
    assert expected == read_response.model


async def test_read_by_id_not_exists(
    api_gateway: TestApiGateway,
    created_student: CreatedStudent,
) -> None:
    read_response = await api_gateway.read_mentor_by_id(created_student.token.access_token, uuid4())
    assert read_response.status_code == 404


async def test_unauthorized(api_gateway: TestApiGateway) -> None:
    response = await api_gateway.read_mentor("")
    assert response.status_code == 401
    assert response.model is None
