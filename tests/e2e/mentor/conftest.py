import pytest

from crudik.application.mentor.interactors.sign_up import MentorContactModel, SignUpMentorRequest


@pytest.fixture
def mentor() -> SignUpMentorRequest:
    return SignUpMentorRequest(
        full_name="Bababyi",
        age=19,
        description="Bababyi experienced",
        contacts=[MentorContactModel(url="ababyiExperienced", social_network="telegram")],
        skills=["experienced", "skills"],
    )
