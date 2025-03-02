from crudik.adapters.test_api_gateway import TestApiGateway
from crudik.application.data_model.mentor import MentorContactModel
from crudik.application.mentor.interactors.sign_up import SignUpMentorRequest
from crudik.application.student.interactors.swipe_mentor import SwipeMentorRequest
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
        skills=["maths", "freebsd", "russian"],
    ),
    SignUpMentorRequest(
        full_name="Vasiliy Skilled 3",
        description="I'm very expierenced mentor",
        contacts=[MentorContactModel(url="ababyiExperienced", social_network="telegram")],
        skills=["english", "maths", "skills"],
    ),
]


async def test_success_read_favorite(
    created_student: CreatedStudent,
    api_gateway: TestApiGateway,
) -> None:
    for mentor in mentors:
        resp = await api_gateway.sign_up_mentor(mentor)
        assert resp.status_code == 200

    response_find_mentor = await api_gateway.find_student(created_student.token.access_token)
    assert response_find_mentor.status_code == 200
    assert response_find_mentor.model is not None
    assert len(response_find_mentor.model) == len(mentors)

    for m in response_find_mentor.model:
        await api_gateway.swipe_mentor(
            student_token=created_student.token.access_token,
            schema=SwipeMentorRequest(
                type=SwipedMentorType.FAVORITES,
                mentor_id=m.id,
            ),
        )

    favorite_response = await api_gateway.read_favorites_mentors(created_student.token.access_token)
    assert favorite_response.status_code == 200
    assert favorite_response.model is not None
    assert len(favorite_response.model) == len(mentors)
