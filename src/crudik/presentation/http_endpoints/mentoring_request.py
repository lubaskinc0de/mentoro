from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from crudik.application.data_model.mentoring_request import MentoringRequestData
from crudik.application.mentoring_request.interactors.read_all import ReadAllMentoringRequest
from crudik.application.mentoring_request.interactors.send import SendMentoring, SendMentoringRequest
from crudik.application.mentoring_request.interactors.verdict import (
    VerdictMentoringRequest,
    VerdictMentoringRequestQuery,
)
from crudik.presentation.http_endpoints.error_model import ErrorModel

router = APIRouter(
    prefix="/mentor/request",
    tags=["Mentoring Requests"],
    route_class=DishkaRoute,
)
security = HTTPBearer(auto_error=False)


@router.post(
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
    schema: SendMentoringRequest,
    interactor: FromDishka[SendMentoring],
    _token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> None:
    """Send mentoring request from favourites."""
    await interactor.execute(schema)


@router.get("")
async def get_all_requests(
    interactor: FromDishka[ReadAllMentoringRequest],
    _token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> list[MentoringRequestData]:
    return await interactor.execute()


@router.post(
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
    interactor: FromDishka[VerdictMentoringRequest],
    _token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> None:
    await interactor.execute(schema)
