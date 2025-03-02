from crudik.adapters.test_api_gateway import TestApiGateway
from crudik.application.data_model.mentor import MentorData
from crudik.application.mentor.interactors.sign_up import SignUpMentorRequest


async def test_success_read(
    mentor: SignUpMentorRequest,
    api_gateway: TestApiGateway,
) -> None:
    sign_in_response = await api_gateway.sign_up_mentor(mentor)
    assert sign_in_response.model is not None

    read_response = await api_gateway.read_mentor(sign_in_response.model.access_token)
    assert read_response.status_code == 200
    assert read_response.model is not None

    expected = MentorData(**mentor.model_dump(), id=read_response.model.id)
    assert expected == read_response.model


async def test_unsuccess_unauthorized(api_gateway: TestApiGateway) -> None:
    response = await api_gateway.read_mentor("")
    assert response.status_code == 401
    assert response.model is None
