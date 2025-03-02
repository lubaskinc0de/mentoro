from crudik.adapters.test_api_gateway import TestApiGateway
from crudik.application.mentor.interactors.sign_in import SignInMentorRequest
from crudik.application.mentor.interactors.sign_up import SignUpMentorRequest


async def test_success_sign_up(
    mentor: SignUpMentorRequest,
    api_gateway: TestApiGateway,
) -> None:
    response = await api_gateway.sign_up_mentor(mentor)
    assert response.model is not None
    response = await api_gateway.sign_in_mentor(
        SignInMentorRequest(full_name="Bababyi"),
    )
    assert response.status_code == 200
