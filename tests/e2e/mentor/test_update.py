from pathlib import Path

from crudik.application.mentor.interactors.sign_up import SignUpMentorRequest
from tests.e2e.gateway import TestApiGateway


async def test_update_mentor_avatar(
    api_gateway: TestApiGateway,
    mentor: SignUpMentorRequest,
) -> None:
    sign_in_response = await api_gateway.sign_up_mentor(mentor)
    assert sign_in_response.status_code == 200
    assert sign_in_response.model is not None

    with Path("./tests/e2e/images/vasiliy-mentor.jpg").open("rb") as f:
        response = await api_gateway.mentor_update_avatar(
            sign_in_response.model.access_token,
            f,
        )

    assert response.status_code == 200
    assert response.model is not None
    assert response.model.photo_url is not None

    me = await api_gateway.read_mentor(sign_in_response.model.access_token)
    assert me.status_code == 200

    assert me.model is not None
    assert me.model.photo_url is not None


async def test_update_mentor_avatar_fail(
    api_gateway: TestApiGateway,
    mentor: SignUpMentorRequest,
) -> None:
    sign_in_response = await api_gateway.sign_up_mentor(mentor)
    assert sign_in_response.status_code == 200
    assert sign_in_response.model is not None

    with Path("./tests/e2e/images/invalid.jpeg").open("rb") as f:
        response = await api_gateway.mentor_update_avatar(
            sign_in_response.model.access_token,
            f,
        )

    assert response.status_code == 400
