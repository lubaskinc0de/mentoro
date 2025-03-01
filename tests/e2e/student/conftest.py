from dataclasses import dataclass

import pytest

from crudik.application.data_model.token_data import TokenResponse
from crudik.application.student.interactors.sign_up import SignUpStudentRequest
from tests.e2e.gateway import TestApiGateway


@dataclass
class CreatedStudent:
    student: SignUpStudentRequest
    token: TokenResponse


@pytest.fixture
async def created_student(api_gateway: TestApiGateway) -> CreatedStudent:
    student = SignUpStudentRequest(full_name="Vasiliy Skilled", age=32, interests=["skills", "freebsd"])
    response = await api_gateway.sign_up_student(student)

    assert response.status_code == 200
    assert response.model is not None

    return CreatedStudent(
        student=student,
        token=response.model,
    )
