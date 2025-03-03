from uuid import uuid4

from crudik.adapters.test_api_gateway import TestApiGateway
from crudik.application.data_model.mentor import MentorContactModel, MentorData
from crudik.application.data_model.mentoring_request import MentoringRequestData
from crudik.application.mentor.sign_up import SignUpMentorRequest
from crudik.application.mentoring_request.send import SendMentoringByUserRequest
from crudik.application.mentoring_request.verdict import VerdictMentoringRequestQuery, VerdictMentoringRequestType
from crudik.models.mentoring_request import MentoringRequestType
from tests.e2e.conftest import CreatedMentor, CreatedStudent


async def get_mentor(api_gateway: TestApiGateway, created_mentor: CreatedMentor) -> MentorData:
    mentor = await api_gateway.read_mentor(created_mentor.token.access_token)

    assert mentor.status_code == 200
    assert mentor.model is not None

    return mentor.model


async def test_send_request_student(
    api_gateway: TestApiGateway, created_student: CreatedStudent, created_mentor: CreatedMentor
) -> None:
    mentor = await get_mentor(api_gateway, created_mentor)

    reponse = await api_gateway.send_mentoring(
        SendMentoringByUserRequest(
            mentor_id=mentor.id,
        ),
        created_student.token.access_token,
    )
    assert reponse.status_code == 200

    requests = await api_gateway.read_student_requests(created_student.token.access_token)

    assert requests.status_code == 200
    assert requests.model is not None

    assert len(requests.model) == 1

    request = requests.model[0]
    mentor.contacts = []

    assert (
        MentoringRequestData(
            mentor=mentor, id=request.id, created_at=request.created_at, type=MentoringRequestType.REVIEW
        )
        == request
    )


async def test_request_ordering(api_gateway: TestApiGateway, created_student: CreatedStudent) -> None:
    mentor_first = SignUpMentorRequest(
        full_name="Vasiliy Skilled",
        description="Vasiliy Skilled description",
        contacts=[MentorContactModel(url="ababyiExperienced", social_network="telegram")],
        skills=["expierence", "freebsd", "english"],
    )
    response_mentor_first = await api_gateway.sign_up_mentor(mentor_first)

    assert response_mentor_first.status_code == 200
    assert response_mentor_first.model is not None

    mentor_second = SignUpMentorRequest(
        full_name="Vasiliy Skilled 1",
        description="Vasiliy Skilled description",
        contacts=[MentorContactModel(url="ababyiExperienced", social_network="telegram")],
        skills=["expierence", "freebsd", "english"],
    )
    response_mentor_second = await api_gateway.sign_up_mentor(mentor_second)

    assert response_mentor_second.status_code == 200
    assert response_mentor_second.model is not None

    reponse_first = await api_gateway.send_mentoring(
        SendMentoringByUserRequest(
            mentor_id=response_mentor_first.model.id,
        ),
        created_student.token.access_token,
    )
    assert reponse_first.status_code == 200

    response_second = await api_gateway.send_mentoring(
        SendMentoringByUserRequest(
            mentor_id=response_mentor_second.model.id,
        ),
        created_student.token.access_token,
    )
    assert response_second.status_code == 200

    requests = await api_gateway.read_student_requests(created_student.token.access_token)
    assert requests.status_code == 200
    assert requests.model is not None

    assert len(requests.model) == 2
    to_accept = next(each for each in requests.model if each.mentor.id == response_mentor_second.model.id)

    response_verdict = await api_gateway.verdict_mentor(
        response_mentor_second.model.access_token,
        VerdictMentoringRequestQuery(mentoring_request_id=to_accept.id, type=VerdictMentoringRequestType.ACCEPTED),
    )
    assert response_verdict.status_code == 200

    requests_second = await api_gateway.read_student_requests(created_student.token.access_token)
    assert requests_second.status_code == 200
    assert requests_second.model is not None

    assert len(requests_second.model) == 2
    assert (requests_second.model[0]).type == MentoringRequestType.REVIEW
    assert (requests_second.model[1]).type == MentoringRequestType.ACCEPTED


async def test_send_request_student_fail(api_gateway: TestApiGateway, created_student: CreatedStudent) -> None:
    reponse = await api_gateway.send_mentoring(
        SendMentoringByUserRequest(
            mentor_id=uuid4(),
        ),
        created_student.token.access_token,
    )
    assert reponse.status_code == 404


async def test_send_request_student_fail_unauthorized(
    api_gateway: TestApiGateway, created_student: CreatedStudent, created_mentor: CreatedMentor
) -> None:
    mentor = await api_gateway.read_mentor(created_mentor.token.access_token)
    assert mentor.status_code == 200
    assert mentor.model is not None

    reponse = await api_gateway.send_mentoring(
        SendMentoringByUserRequest(
            mentor_id=mentor.model.id,
        ),
        created_student.token.access_token[:-1],
    )
    assert reponse.status_code == 401


async def test_delete_request_student(
    api_gateway: TestApiGateway, created_student: CreatedStudent, created_mentor: CreatedMentor
) -> None:
    mentor = await get_mentor(api_gateway, created_mentor)

    reponse = await api_gateway.send_mentoring(
        SendMentoringByUserRequest(
            mentor_id=mentor.id,
        ),
        created_student.token.access_token,
    )
    assert reponse.status_code == 200

    requests = await api_gateway.read_student_requests(created_student.token.access_token)

    assert requests.status_code == 200
    assert requests.model is not None

    assert len(requests.model) == 1

    del_request = await api_gateway.delete_mentoring_request(created_student.token.access_token, requests.model[0].id)

    assert del_request.status_code == 200
