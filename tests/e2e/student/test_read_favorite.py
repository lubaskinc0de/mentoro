from crudik.adapters.test_api_gateway import TestApiGateway
from crudik.application.data_model.mentor import MentorContactModel
from crudik.application.mentor.interactors.sign_up import SignUpMentorRequest
from crudik.application.student.interactors.swipe_mentor import SwipeMentorRequest
from crudik.models.swiped_mentor import SwipedMentorType
from tests.e2e.student.conftest import CreatedStudent

mentors = [
    SignUpMentorRequest(
        full_name="Vasiliy Skilled 1",
        age=32,
        description="I'm very expierenced mentor",
        contacts=[MentorContactModel(url="ababyiExperienced", social_network="telegram")],
        skills=["expierence", "freebsd", "english"],
    ),
    SignUpMentorRequest(
        full_name="Vasiliy Skilled 2",
        age=32,
        description="I'm very expierenced mentor",
        contacts=[MentorContactModel(url="ababyiExperienced", social_network="telegram")],
        skills=["maths", "freebsd", "russian"],
    ),
    SignUpMentorRequest(
        full_name="Vasiliy Skilled 3",
        age=32,
        description="I'm very expierenced mentor",
        contacts=[MentorContactModel(url="ababyiExperienced", social_network="telegram")],
        skills=["english", "maths"],
    ),
    SignUpMentorRequest(
        full_name="Vasiliy Skilled 4",
        age=32,
        description="I'm very expierenced mentor",
        contacts=[MentorContactModel(url="ababyiExperienced", social_network="telegram")],
        skills=["english", "russian"],
    ),
]


async def test_success_read_favorite(
    created_student: CreatedStudent,
    api_gateway: TestApiGateway,
) -> None:
    for mentor in mentors:
        await api_gateway.sign_up_mentor(mentor)

    for _ in mentors:
        response_find_mentor = await api_gateway.find_student(created_student.token.access_token)

        assert response_find_mentor.status_code == 200
        assert response_find_mentor.model is not None

        await api_gateway.swipe_mentor(
            student_token=created_student.token.access_token,
            schema=SwipeMentorRequest(
                type=SwipedMentorType.FAVORITES,
                mentor_id=response_find_mentor.model.id,
            ),
        )

    favorite_response = await api_gateway.read_favorites_mentors(created_student.token.access_token)
    assert favorite_response.status_code == 200
    assert favorite_response.model is not None
    assert len(favorite_response.model) == len(mentors)
