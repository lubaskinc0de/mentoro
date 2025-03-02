from crudik.adapters.test_api_gateway import TestApiGateway
from crudik.application.data_model.mentoring_request import MentoringRequestData
from crudik.application.mentoring_request.interactors.send import SendMentoringRequest
from crudik.models.mentoring_request import MentoringRequestType
from tests.e2e.conftest import CreatedMentor, CreatedStudent


async def test_send_request_student(
    api_gateway: TestApiGateway, created_student: CreatedStudent, created_mentor: CreatedMentor
) -> None:
    mentor = await api_gateway.read_mentor(created_mentor.token.access_token)
    assert mentor.status_code == 200
    assert mentor.model is not None

    reponse = await api_gateway.send_mentoring(
        SendMentoringRequest(
            mentor_id=mentor.model.id,
        ),
        created_student.token.access_token,
    )
    assert reponse.status_code == 200

    requests = await api_gateway.read_student_requests(created_student.token.access_token)

    assert requests.status_code == 200
    assert requests.model is not None

    assert len(requests.model) == 1

    request = requests.model[0]

    assert (
        MentoringRequestData(
            mentor=mentor.model, id=request.id, created_at=request.created_at, type=MentoringRequestType.REVIEW
        )
        == request
    )
