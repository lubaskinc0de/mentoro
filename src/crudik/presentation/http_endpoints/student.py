from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Response
from pydantic import BaseModel
from typing_extensions import Doc

from crudik.application.student.errors import IncorrectLengthStudentLoginError
from crudik.application.student.interactors.sign_up import SignUpStudent
from crudik.presentation.http_endpoints.common import ErrorResponse

router = APIRouter(
    route_class=DishkaRoute,
    tags=["Student"],
)


class SignUpStudentRequest(BaseModel):
    login: Annotated[str, Doc("Student login")]
    full_name: Annotated[str, Doc("Student full name")]
    password: Annotated[str, Doc("Student password")]


class SignUpStudentResponse(BaseModel):
    access_token: Annotated[str, Doc("Student access token")]


@router.post(
    "/student/sign_up",
    responses={
        "201": {
            "model": SignUpStudentResponse,
            "description": "Success response schema",
        },
        "422": {
            "model": ErrorResponse,
            "description": "Invalid request data",
        },
    },
)
async def sign_up_student(
    schema: SignUpStudentRequest,
    interactor: FromDishka[SignUpStudent],
) -> Response:
    try:
        access_token = await interactor.execute(
            login=schema.login,
            full_name=schema.full_name,
            password=schema.password,
        )
    except IncorrectLengthStudentLoginError:
        return Response(
            status_code=422,
            content=ErrorResponse(
                error="Incorrect length student login",
            ).model_dump_json(),
        )
    return Response(
        status_code=201,
        content=SignUpStudentResponse(
            access_token=access_token,
        ).model_dump_json(),
    )
