from crudik.adapters.test_api_gateway import TestApiGateway
from crudik.application.mentor.interactors.sign_up import MentorContactModel, SignUpMentorRequest
from crudik.application.student.interactors.sign_up import SignUpStudentRequest


async def test_student_getme_fail(api_gateway: TestApiGateway) -> None:
    response = await api_gateway.student_get_me("invalid_token")
    assert response.status_code == 401


async def test_read_by_id(api_gateway: TestApiGateway) -> None:
    student_data = SignUpStudentRequest(full_name="Bybyba", interests=["bybyba"])
    sign_up_student_response = await api_gateway.sign_up_student(student_data)

    assert sign_up_student_response.model is not None
    assert sign_up_student_response.status_code == 200

    student_id = sign_up_student_response.model.id
    mentor_data = SignUpMentorRequest(
        full_name="Vasiliy Skilled 1",
        age=32,
        description="I'm very expierenced mentor",
        contacts=[
            MentorContactModel(
                social_network="tg",
                url="https://t.me/lubaskinc0de",
            ),
        ],
        skills=["expierence", "freebsd", "english"],
    )
    sign_up_mentor_response = await api_gateway.sign_up_mentor(mentor_data)
    assert sign_up_mentor_response.status_code == 200
    assert sign_up_mentor_response.model is not None

    mentor_token = sign_up_mentor_response.model.access_token
    get_student_response = await api_gateway.student_get_by_id(
        mentor_token,
        student_id,
    )
    student = get_student_response.model
    assert student is not None

    assert student.full_name == student_data.full_name
    assert student.id == student_id
    assert student.interests == student_data.interests
