from crudik.adapters.test_api_gateway import TestApiGateway
from crudik.application.data_model.mentor import MentorContactModel, MentorData
from crudik.application.mentor.sign_up import SignUpMentorRequest
from crudik.application.student.swipe_mentor import SwipeMentorRequest
from crudik.models.swiped_mentor import SwipedMentorType
from tests.e2e.conftest import CreatedStudent

mentors = [
    SignUpMentorRequest(
        full_name="Vasiliy Skilled 1",
        description="I'm very expierenced mentor",
        contacts=[MentorContactModel(url="ababyiExperienced", social_network="telegram")],
        skills=["expierence", "freebsd", "english"],
    ),
    SignUpMentorRequest(
        full_name="Vasiliy Skilled 2",
        description="I'm very expierenced mentor",
        contacts=[MentorContactModel(url="ababyiExperienced", social_network="telegram")],
        skills=["expierence", "freebsd", "english"],
    ),
    SignUpMentorRequest(
        full_name="Vasiliy Skilled 3",
        description="I'm very expierenced mentor",
        contacts=[MentorContactModel(url="ababyiExperienced", social_network="telegram")],
        skills=["expierence", "freebsd", "english"],
    ),
]


async def test_success_read_favorite(
    created_student: CreatedStudent,
    api_gateway: TestApiGateway,
) -> None:
    student_token = created_student.token.access_token
    for mentor in mentors:
        await api_gateway.sign_up_mentor(mentor)

    finded_mentors: list[MentorData] = []
    for _ in mentors:
        response_find_mentor = await api_gateway.find_student(student_token)

        assert response_find_mentor.status_code == 200
        assert response_find_mentor.model is not None

        finded_mentors.append(response_find_mentor.model[0])

        await api_gateway.swipe_mentor(
            student_token=student_token,
            schema=SwipeMentorRequest(
                type=SwipedMentorType.FAVORITES,
                mentor_id=response_find_mentor.model[0].id,
            ),
        )

    deleting = finded_mentors[-1]
    await api_gateway.delete_favorites_mentors(
        student_token=student_token,
        mentor_id=deleting.id,
    )

    favorite_response = await api_gateway.read_favorites_mentors(created_student.token.access_token)

    assert favorite_response.status_code == 200
    assert favorite_response.model is not None
    assert len(favorite_response.model) == len(mentors) - 1
    for finded_mentor in favorite_response.model:
        assert finded_mentor != deleting
