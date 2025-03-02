import pytest

from crudik.application.data_model.mentor import MentorContactModel
from crudik.application.mentor.sign_up import SignUpMentorRequest


@pytest.fixture
def mentor() -> SignUpMentorRequest:
    return SignUpMentorRequest(
        full_name="Bababyi",
        description="Bababyi experienced",
        contacts=[MentorContactModel(url="ababyiExperienced", social_network="telegram")],
        skills=["experienced", "skills"],
    )
