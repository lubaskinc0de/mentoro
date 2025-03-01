from crudik.application.mentor.interactors.sign_in import SignInMentorRequest
from crudik.application.mentor.interactors.sign_up import SignUpMentorRequest
from filler.test_gateway import TestApiGateway


async def test_success_sign_in(
    mentor: SignUpMentorRequest,
    api_gateway: TestApiGateway,
) -> None:
    sign_in_response = await api_gateway.sign_up_mentor(mentor)
    assert sign_in_response.model is not None

    sign_up_response = await api_gateway.sign_in_mentor(
        SignInMentorRequest(full_name="Bababyi"),
    )
    assert sign_up_response.model is not None


async def test_unsuccess_sign_in(api_gateway: TestApiGateway) -> None:
    response = await api_gateway.sign_in_mentor(
        SignInMentorRequest(full_name="Bababyi"),
    )
    assert response.status_code == 404
