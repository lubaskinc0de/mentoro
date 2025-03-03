from dataclasses import dataclass
from uuid import uuid4

from crudik.adapters.test_api_gateway import TestApiGateway
from crudik.application.data_model.mentor import MentorData
from crudik.application.data_model.mentoring_request import MentoringRequestData
from crudik.application.mentoring_request.send import SendMentoringByUserRequest
from crudik.application.mentoring_request.verdict import VerdictMentoringRequestQuery, VerdictMentoringRequestType
from crudik.application.review.add_review import ReviewCreateData
from tests.e2e.conftest import CreatedMentor, CreatedStudent
from tests.e2e.student.test_request import get_mentor


@dataclass
class PreparationData:
    mentor: MentorData
    requests: list[MentoringRequestData]


async def preparation_data(
    api_gateway: TestApiGateway,
    created_student: CreatedStudent,
    created_mentor: CreatedMentor,
) -> PreparationData:
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

    return PreparationData(mentor=mentor, requests=requests.model)


async def test_add_review(
    api_gateway: TestApiGateway, created_student: CreatedStudent, created_mentor: CreatedMentor
) -> None:
    data = await preparation_data(api_gateway, created_student, created_mentor)
    request_id = data.requests[0].id
    response = await api_gateway.verdict_mentor(
        created_mentor.token.access_token,
        VerdictMentoringRequestQuery(mentoring_request_id=request_id, type=VerdictMentoringRequestType.ACCEPTED),
    )
    assert response.status_code == 200

    review_response = await api_gateway.add_review(
        created_student.token.access_token,
        ReviewCreateData(
            mentor_id=data.mentor.id,
            text="He was very experienced!",
            rate=5,
        ),
    )

    assert review_response.status_code == 200

    reviews = await api_gateway.read_reviews(
        created_student.token.access_token,
        data.mentor.id,
    )

    assert reviews.status_code == 200
    assert reviews.model is not None

    review = reviews.model[0]

    assert review.mentor == data.mentor
    assert review.text == "He was very experienced!"
    assert review.rate == 5


async def test_student_not_found(
    api_gateway: TestApiGateway, created_student: CreatedStudent, created_mentor: CreatedMentor
) -> None:
    data = await preparation_data(api_gateway, created_student, created_mentor)

    request_id = data.requests[0].id
    response = await api_gateway.verdict_mentor(
        created_mentor.token.access_token,
        VerdictMentoringRequestQuery(
            mentoring_request_id=request_id,
            type=VerdictMentoringRequestType.ACCEPTED,
        ),
    )
    assert response.status_code == 200

    review_response = await api_gateway.add_review(
        "Not access token",
        ReviewCreateData(
            mentor_id=data.mentor.id,
            text="He was very experienced!",
            rate=5,
        ),
    )

    assert review_response.status_code == 401


async def test_mentor_not_found(
    api_gateway: TestApiGateway, created_student: CreatedStudent, created_mentor: CreatedMentor
) -> None:
    data = await preparation_data(api_gateway, created_student, created_mentor)

    response = await api_gateway.verdict_mentor(
        created_mentor.token.access_token,
        VerdictMentoringRequestQuery(
            mentoring_request_id=data.requests[0].id,
            type=VerdictMentoringRequestType.ACCEPTED,
        ),
    )
    assert response.status_code == 200

    review_response = await api_gateway.add_review(
        created_student.token.access_token,
        ReviewCreateData(
            mentor_id=uuid4(),
            text="He was very experienced!",
            rate=5,
        ),
    )

    assert review_response.status_code == 404


async def test_mentoring_request_not_accepted(
    api_gateway: TestApiGateway, created_student: CreatedStudent, created_mentor: CreatedMentor
) -> None:
    data = await preparation_data(api_gateway, created_student, created_mentor)

    review_response = await api_gateway.add_review(
        created_student.token.access_token,
        ReviewCreateData(mentor_id=data.mentor.id, text="He was very experienced!", rate=5),
    )

    assert review_response.status_code == 403
