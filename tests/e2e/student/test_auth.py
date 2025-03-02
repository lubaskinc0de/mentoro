from crudik.adapters.test_api_gateway import TestApiGateway
from crudik.application.data_model.student import StudentData
from crudik.application.student.interactors.sign_in import SignInStudentRequest
from crudik.application.student.interactors.sign_up import SignUpStudentRequest
from tests.e2e.conftest import CreatedStudent


async def test_student_signup(api_gateway: TestApiGateway) -> None:
    student = SignUpStudentRequest(full_name="Vasiliy Skilled", age=32, interests=["skills", "freebsd"])

    response = await api_gateway.sign_up_student(student)

    assert response.status_code == 200
    assert response.model is not None

    me = await api_gateway.student_get_me(response.model.access_token)

    assert me.status_code == 200
    assert me.model is not None
    assert StudentData(**student.model_dump(), id=me.model.id) == me.model


async def test_student_signin(api_gateway: TestApiGateway, created_student: CreatedStudent) -> None:
    student_login_req = SignInStudentRequest(full_name=created_student.student.full_name)
    response = await api_gateway.sign_in_student(student_login_req)
    assert response.status_code == 200
    assert response.model is not None

    me = await api_gateway.student_get_me(response.model.access_token)
    assert me.status_code == 200

    assert me.model is not None
    assert StudentData(**created_student.student.model_dump(), id=me.model.id) == me.model


async def test_student_signin_fail(api_gateway: TestApiGateway) -> None:
    response = await api_gateway.sign_in_student(SignInStudentRequest(full_name="Vasiliy UnSkilled"))
    assert response.status_code == 401
