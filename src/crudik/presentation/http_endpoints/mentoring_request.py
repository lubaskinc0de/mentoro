from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from crudik.application.data_model.mentoring_request import MentoringRequestData
from crudik.application.mentoring_request.interactors.read_all import ReadStudentMentoringRequest
from crudik.application.mentoring_request.interactors.send import SendMentoringByStudent, SendMentoringByUserRequest
from crudik.application.mentoring_request.interactors.verdict import (
    VerdictMentoringRequestByMentor,
    VerdictMentoringRequestQuery,
)
from crudik.presentation.http_endpoints.error_model import ErrorModel

mentor_router = APIRouter(
    prefix="/mentor/request",
    tags=["Mentoring Requests"],
    route_class=DishkaRoute,
)
student_router = APIRouter(
    prefix="/student/request",
    tags=["Student Requests"],
    route_class=DishkaRoute,
)
security = HTTPBearer(auto_error=False)


@mentor_router.post(
    "",
    responses={
        404: {
            "description": "Mentor not found",
            "model": ErrorModel,
        },
        401: {
            "description": "Unauthorized",
            "model": ErrorModel,
        },
    },
)
async def send_mentoring(
    schema: SendMentoringByUserRequest,
    interactor: FromDishka[SendMentoringByStudent],
    _token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> None:
    """Send mentoring request from favourites."""
    await interactor.execute(schema)


@student_router.get("")
async def get_all_requests(
    interactor: FromDishka[ReadStudentMentoringRequest],
    _token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> list[MentoringRequestData]:
    return await interactor.execute()


@mentor_router.post(
    "/verdict",
    responses={
        404: {
            "description": "Mentor not found",
            "model": ErrorModel,
        },
        401: {
            "description": "Unauthorized",
            "model": ErrorModel,
        },
    },
)
async def verdict_mentoring_request(
    schema: VerdictMentoringRequestQuery,
    interactor: FromDishka[VerdictMentoringRequestByMentor],
    _token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> None:
    await interactor.execute(schema)
