from pathlib import Path

from crudik.application.student.interactors.update import UpdateStudentRequest
from filler.test_gateway import TestApiGateway
from tests.e2e.student.conftest import CreatedStudent


async def test_update_student_avatar(api_gateway: TestApiGateway, created_student: CreatedStudent) -> None:
    with Path("./tests/e2e/images/vasiliy.jpg").open("rb") as f:
        response = await api_gateway.student_update_avatar(
            created_student.token.access_token,
            f,
        )

    assert response.status_code == 200
    assert response.model is not None
    assert response.model.avatar_url is not None

    me = await api_gateway.student_get_me(created_student.token.access_token)
    assert me.status_code == 200

    assert me.model is not None
    assert me.model.avatar_url is not None


async def test_update_student_avatar_fail(api_gateway: TestApiGateway, created_student: CreatedStudent) -> None:
    with Path("./tests/e2e/images/invalid.jpeg").open("rb") as f:
        response = await api_gateway.student_update_avatar(
            created_student.token.access_token,
            f,
        )

    assert response.status_code == 400


async def test_update_student_fail(api_gateway: TestApiGateway, created_student: CreatedStudent) -> None:
    response = await api_gateway.student_update(
        created_student.token.access_token,
        UpdateStudentRequest(age=33, interests=["skills", "freebsd", "experience"]),
    )

    assert response.status_code == 200

    me = await api_gateway.student_get_me(created_student.token.access_token)
    assert me.status_code == 200

    assert me.model is not None
    assert me.model.age == 33
    assert me.model.interests == ["skills", "freebsd", "experience"]
    assert me.model.full_name == created_student.student.full_name
