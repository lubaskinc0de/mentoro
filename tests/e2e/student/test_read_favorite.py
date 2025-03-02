from crudik.adapters.test_api_gateway import TestApiGateway
from crudik.application.mentor.interactors.sign_up import SignUpMentorRequest
from tests.e2e.student.conftest import CreatedMentor, CreatedStudent


async def test_success_read_favorite(
    created_student: CreatedStudent,
    created_mentor: CreatedMentor,
    api_gateway: TestApiGateway,
) -> None:
    
    

