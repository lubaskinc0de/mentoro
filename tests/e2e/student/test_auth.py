from crudik.application.student.interactors.sign_in import SignInStudentRequest
from crudik.application.student.interactors.sign_up import SignUpStudentRequest
from tests.e2e.gateway import TestApiGateway


async def test_student_signup(api_gateway: TestApiGateway) -> None:
    student = SignUpStudentRequest(full_name="Vasiliy Skilled", age=32, interests=["skills", "freebsd"])

    response = await api_gateway.sign_up_client(student)

    assert response.status_code == 200
    assert response.model is not None

    me = await api_gateway.student_get_me(response.model.access_token)

    assert me.status_code == 200

    assert me.model is not None

    assert me.model.full_name == "Vasiliy Skilled"
    assert me.model.age == 32
    assert me.model.interests == ["skills", "freebsd"]
    assert me.model.avatar_url is None


async def test_student_signin(api_gateway: TestApiGateway) -> None:
    full_name = "Vasiliy Skilled"
    student = SignUpStudentRequest(full_name=full_name, age=32, interests=["skills", "freebsd"])

    response = await api_gateway.sign_up_client(student)
    assert response.status_code == 200

    response = await api_gateway.sign_in_client(SignInStudentRequest(full_name=full_name))
    assert response.status_code == 200
    assert response.model is not None

    me = await api_gateway.student_get_me(response.model.access_token)
    assert me.status_code == 200

    assert me.model is not None

    assert me.model.full_name == "Vasiliy Skilled"
    assert me.model.age == 32
    assert me.model.interests == ["skills", "freebsd"]
    assert me.model.avatar_url is None


async def test_student_signin_fail(api_gateway: TestApiGateway) -> None:
    response = await api_gateway.sign_in_client(SignInStudentRequest(full_name="Vasiliy UnSkilled"))
    assert response.status_code == 404


async def test_student_getme_fail(api_gateway: TestApiGateway) -> None:
    response = await api_gateway.student_get_me("invalid_token")
    assert response.status_code == 401