from dataclasses import dataclass

import pytest

from crudik.adapters.test_api_gateway import TestApiGateway
from crudik.application.data_model.token_data import TokenResponse
from crudik.application.mentor.interactors.sign_up import SignUpMentorRequest
from crudik.application.student.interactors.sign_up import SignUpStudentRequest


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


@dataclass
class CreatedMentor:
    mentor: SignUpMentorRequest
    token: TokenResponse


@pytest.fixture
async def created_mentor(api_gateway: TestApiGateway) -> CreatedMentor:
    mentor = SignUpMentorRequest(full_name="Vasiliy Skilled", skills=['skills', 'freebsd'], contacts=["skills", "freebsd"])
    response = await api_gateway.sign_up_mentor(mentor)

    assert response.status_code == 200
    assert response.model is not None

    return CreatedMentor(
        mentor=mentor,
        token=response.model,
    )

