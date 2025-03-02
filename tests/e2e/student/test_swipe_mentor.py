from dataclasses import dataclass
from uuid import UUID

import pytest

from crudik.adapters.test_api_gateway import TestApiGateway
from crudik.application.mentor.interactors.sign_up import SignUpMentorRequest
from crudik.application.student.interactors.sign_up import SignUpStudentRequest
from crudik.application.student.interactors.swipe_mentor import SwipeMentorRequest
from crudik.models.swiped_mentor import SwipedMentorType


@dataclass
class DataForSwipe:
    mentor_id: UUID
    student_token: str


@pytest.fixture
async def data_for_swipe(api_gateway: TestApiGateway) -> DataForSwipe:
    sign_up_mentor_response = await api_gateway.sign_up_mentor(
        SignUpMentorRequest(
            full_name="Bybyba",
            contacts=["bybyba"],
            skills=["bybyba"],
        ),
    )
    assert sign_up_mentor_response.model is not None
    mentor_token = sign_up_mentor_response.model.access_token

    read_mentor_response = await api_gateway.read_mentor(mentor_token)
    assert read_mentor_response.model is not None
    mentor = read_mentor_response.model

    sign_up_student_response = await api_gateway.sign_up_student(
        SignUpStudentRequest(
            full_name="Bybyba",
            interests=["bybyba"],
        ),
    )
    assert sign_up_student_response.model is not None
    student_token = sign_up_student_response.model.access_token

    return DataForSwipe(
        mentor_id=mentor.id,
        student_token=student_token,
    )


@pytest.mark.parametrize(
    ("swiped_mentor_type"),
    [
        (SwipedMentorType.DISLIKE),
        (SwipedMentorType.FAVORITES),
        (SwipedMentorType.LIKE),
    ],
)
async def test_success_swipe(
    data_for_swipe: DataForSwipe,
    api_gateway: TestApiGateway,
    swiped_mentor_type: SwipedMentorType,
) -> None:
    response = await api_gateway.swipe_mentor(
        student_token=data_for_swipe.student_token,
        schema=SwipeMentorRequest(
            type=swiped_mentor_type,
            mentor_id=data_for_swipe.mentor_id,
        ),
    )

    assert response.status_code == 200
