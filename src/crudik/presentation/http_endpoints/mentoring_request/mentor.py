from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from crudik.application.data_model.mentoring_request import MentoringRequestMentorData
from crudik.application.mentoring_request.read_all_mentor import ReadMentorMentoringRequests
from crudik.application.mentoring_request.verdict import (
    VerdictMentoringRequestByMentor,
    VerdictMentoringRequestQuery,
)
from crudik.presentation.http_endpoints.error_model import ErrorModel

router = APIRouter(
    prefix="/mentor/request",
    tags=["Заявки которые отправили ментору"],
    route_class=DishkaRoute,
)
security = HTTPBearer(auto_error=False)


@router.post(
    "/verdict",
    description="Принятие или отклонение заявки на ментерство",
    responses={
        200: {
            "description": "Заявка успешно обработана",
        },
        404: {
            "description": "Ментор не найден",
            "model": ErrorModel,
        },
        401: {
            "description": "Ментор не авторизован",
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


@router.get(
    "",
    description="Получение менторов всех запросов на менторство студентов",
    responses={
        401: {
            "description": "Ментор не авторизован",
            "model": ErrorModel,
        },
    },
)
async def get_all_requests(
    interactor: FromDishka[ReadMentorMentoringRequests],
    _token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> list[MentoringRequestMentorData]:
    return await interactor.execute()
