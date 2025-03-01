from tests.e2e.gateway import TestApiGateway


async def test_student_getme_fail(api_gateway: TestApiGateway) -> None:
    response = await api_gateway.student_get_me("invalid_token")
    assert response.status_code == 401
