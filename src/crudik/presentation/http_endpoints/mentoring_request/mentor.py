from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from crudik.application.mentoring_request.verdict import (
    VerdictMentoringRequestByMentor,
    VerdictMentoringRequestQuery,
)
from crudik.presentation.http_endpoints.error_model import ErrorModel

router = APIRouter(
    prefix="/mentor/request",
    tags=["Заявки ментора на ментерство"],
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
