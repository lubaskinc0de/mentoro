import pytest

from crudik.adapters.test_api_gateway import TestApiGateway
from crudik.application.data_model.mentor import MentorContactModel
from crudik.application.mentor.sign_up import SignUpMentorRequest
from crudik.application.student.sign_up import SignUpStudentRequest

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
        skills=["english", "maths"],
    ),
    SignUpMentorRequest(
        full_name="Vasiliy Skilled 4",
        description="I'm very expierenced mentor",
        contacts=[MentorContactModel(url="ababyiExperienced", social_network="telegram")],
        skills=["english", "russian"],
    ),
]


@pytest.mark.parametrize(
    ("mentor_full_name", "student"),
    [
        (
            "Vasiliy Skilled 1",
            SignUpStudentRequest(full_name="Vasya Lopuh 1", age=32, interests=["expieren", "freebd"]),
        ),
        ("Vasiliy Skilled 2", SignUpStudentRequest(full_name="Vasya Lopuh 2", age=32, interests=["russin", "freebsd"])),
        ("Vasiliy Skilled 3", SignUpStudentRequest(full_name="Vasya Lopuh 3", age=32, interests=["math", "english"])),
        ("Vasiliy Skilled 4", SignUpStudentRequest(full_name="Vasya Lopuh 4", age=32, interests=["englis", "russia"])),
        ("Vasiliy Skilled 1", SignUpStudentRequest(full_name="Vasya Lopuh 5", age=32, interests=["exp", "freebsd"])),
    ],
)
async def test_student_find(
    api_gateway: TestApiGateway,
    mentor_full_name: str,
    student: SignUpStudentRequest,
) -> None:
    for mentor in mentors:
        response = await api_gateway.sign_up_mentor(mentor)
        assert response.status_code == 200

    response = await api_gateway.sign_up_student(student)
    assert response.status_code == 200
    assert response.model is not None

    feed = await api_gateway.find_student(response.model.access_token)
    assert feed.status_code == 200

    assert feed.model is not None
    assert feed.model[0].full_name == mentor_full_name
