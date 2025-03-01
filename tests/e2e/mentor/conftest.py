import pytest

from crudik.application.mentor.interactors.sign_up import SignUpMentorRequest


@pytest.fixture
def mentor() -> SignUpMentorRequest:
    return SignUpMentorRequest(
        full_name="Bababyi",
        age=19,
        description="Bababyi experienced",
        contacts=["tg: @BababyiExperienced", "vk: @BababyiExperienced"],
        skills=["experienced", "skills"],
    )
