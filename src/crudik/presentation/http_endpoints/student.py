from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from crudik.application.data_model.token_data import TokenResponse
from crudik.application.student.interactors.sign_up import SignUpStudent, SignUpStudentRequest

router = APIRouter(
    route_class=DishkaRoute,
    tags=["Student"],
)


@router.post("/student/sign_up")
async def sign_up_student(
    schema: SignUpStudentRequest,
    interactor: FromDishka[SignUpStudent],
) -> TokenResponse:
    return await interactor.execute(schema)
