from crudik.application.mentor.interactors.sign_up import SignUpMentorRequest
from tests.e2e.gateway import TestApiGateway


async def test_success_read(
    mentor: SignUpMentorRequest,
    api_gateway: TestApiGateway,
) -> None:
    sign_in_response = await api_gateway.sign_up_mentor(mentor)
    assert sign_in_response.model is not None
    
    read_response = await api_gateway.read_mentor(sign_in_response.model.access_token)
    assert read_response.status_code == 200
    assert read_response.model is not None


async def test_unsuccess_unauthorizated(api_gateway: TestApiGateway) -> None:
    response = await api_gateway.read_mentor("")
    assert response.status_code == 400
    assert response.model is None
