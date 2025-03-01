from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from crudik.application.data_model.token_data import TokenResponse
from crudik.application.mentor.interactors.sign_in import SignInMentor, SignInMentorRequest
from crudik.application.mentor.interactors.sign_up import SignUpMentor, SignUpMentorRequest
from crudik.presentation.http_endpoints.error_model import ErrorModel

router = APIRouter(
    route_class=DishkaRoute,
    tags=["Mentor"],
    prefix="/mentor",
)


@router.post("/sign_up")
async def sign_up_mentor(
    schema: SignUpMentorRequest,
    interactor: FromDishka[SignUpMentor],
) -> TokenResponse:
    """Mentor registration."""
    return await interactor.execute(schema)


@router.post(
    "/sign_in",
    responses={
        404: {
            "description": "Student not found",
            "model": ErrorModel,
        },
    },
)
async def sign_in_mentor(
    schema: SignInMentorRequest,
    interactor: FromDishka[SignInMentor],
) -> TokenResponse:
    """Mentor authorisation."""
    return await interactor.execute(schema)
