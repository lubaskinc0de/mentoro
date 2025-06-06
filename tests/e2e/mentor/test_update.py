from importlib.resources import files
from pathlib import Path

import tests.e2e.images
from crudik.adapters.test_api_gateway import TestApiGateway
from crudik.application.data_model.mentor import MentorContactModel, MentorData
from crudik.application.mentor.sign_up import SignUpMentorRequest
from crudik.application.mentor.update import UpdateMentorRequest


async def test_update_mentor_avatar(
    api_gateway: TestApiGateway,
    mentor: SignUpMentorRequest,
) -> None:
    sign_in_response = await api_gateway.sign_up_mentor(mentor)
    assert sign_in_response.status_code == 200
    assert sign_in_response.model is not None

    image_dir = files(tests.e2e.images)

    with Path(str(image_dir / "vasiliy-mentor.jpg")).open("rb") as f:
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

    image_dir = files(tests.e2e.images)

    with Path(str(image_dir / "invalid.jpeg")).open("rb") as f:
        response = await api_gateway.mentor_update_avatar(
            sign_in_response.model.access_token,
            f,
        )

    assert response.status_code == 400


async def test_update_mentor(api_gateway: TestApiGateway, mentor: SignUpMentorRequest) -> None:
    sign_in_response = await api_gateway.sign_up_mentor(mentor)
    assert sign_in_response.status_code == 200
    assert sign_in_response.model is not None

    mentor.description = "Updated description"
    mentor.contacts = [
        MentorContactModel(url="ababyiExperienced", social_network="telegram"),
    ]
    mentor.skills = ["experienced", "skills"]

    response = await api_gateway.update_mentor(
        sign_in_response.model.access_token,
        UpdateMentorRequest(description=mentor.description, contacts=mentor.contacts, skills=mentor.skills),
    )

    assert response.status_code == 200

    me = await api_gateway.read_mentor(sign_in_response.model.access_token)
    assert me.status_code == 200

    assert me.model is not None
    assert me.model == MentorData(**mentor.model_dump(), id=me.model.id)


async def test_update_mentor_unauthorized(api_gateway: TestApiGateway, mentor: SignUpMentorRequest) -> None:
    response = await api_gateway.update_mentor(
        "adjaldjoa",
        UpdateMentorRequest(description=mentor.description, contacts=mentor.contacts, skills=mentor.skills),
    )

    assert response.status_code == 401
