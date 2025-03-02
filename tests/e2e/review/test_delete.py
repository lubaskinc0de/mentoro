from crudik.adapters.test_api_gateway import TestApiGateway
from crudik.application.mentoring_request.send import SendMentoringByUserRequest
from crudik.application.mentoring_request.verdict import VerdictMentoringRequestQuery, VerdictMentoringRequestType
from crudik.application.review.add_review import ReviewCreateData
from tests.e2e.conftest import CreatedMentor, CreatedStudent
from tests.e2e.student.test_request import get_mentor


async def test_delete_review(
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

    request_id = requests.model[0].id
    response = await api_gateway.verdict_mentor(
        created_mentor.token.access_token,
        VerdictMentoringRequestQuery(mentoring_request_id=request_id, type=VerdictMentoringRequestType.ACCEPTED),
    )
    assert response.status_code == 200

    review_response = await api_gateway.add_review(
        created_student.token.access_token,
        ReviewCreateData(mentor_id=mentor.id, text="He was very experienced!", rate=5),
    )
    assert review_response.status_code == 200

    assert review_response.model is not None

    resp = await api_gateway.delete_review(created_student.token.access_token, review_response.model.review_id)
    assert resp.status_code == 200

    resp_two = await api_gateway.delete_review(created_student.token.access_token, review_response.model.review_id)
    assert resp_two.status_code == 404
