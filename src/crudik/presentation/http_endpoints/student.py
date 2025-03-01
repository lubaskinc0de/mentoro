from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from crudik.application.data_model.token_data import TokenResponse
from crudik.application.student.interactors.sign_in import SignInStudent, SignInStudentRequest
from crudik.application.student.interactors.sign_up import SignUpStudent, SignUpStudentRequest
from crudik.presentation.http_endpoints.error_model import ErrorModel

router = APIRouter(
    route_class=DishkaRoute,
    tags=["Student"],
    prefix="/student",
)


@router.post("/sign_up")
async def sign_up_student(
    schema: SignUpStudentRequest,
    interactor: FromDishka[SignUpStudent],
) -> TokenResponse:
    """Регистрация пользователя."""
    return await interactor.execute(schema)


@router.post("/sign_in", responses={
    404: {
        "description": "Student not found",
        "model": ErrorModel,
    },
})
async def sign_in_student(
    schema: SignInStudentRequest,
    interactor: FromDishka[SignInStudent],
) -> TokenResponse:
    """Логин пользователя."""
    return await interactor.execute(schema)
