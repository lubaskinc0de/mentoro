from crudik.application.mentor.interactors.sign_in import SignInMentorRequest
from crudik.application.mentor.interactors.sign_up import SignUpMentorRequest
from tests.e2e.gateway import TestApiGateway


async def test_success_sign_up(
    mentor: SignUpMentorRequest,
    api_gateway: TestApiGateway,
) -> None:
    response = await api_gateway.sign_up_mentor(mentor)
    assert response.model is not None
    response = await api_gateway.sign_in_mentor(
        SignInMentorRequest(full_name="Bababyi"),
    )

