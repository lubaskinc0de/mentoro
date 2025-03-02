from typing import Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, Path
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from crudik.application.data_model.mentoring_request import MentoringRequestData
from crudik.application.mentoring_request.delete import DeleteMentoringRequestById
from crudik.application.mentoring_request.read_all_student import ReadStudentMentoringRequests
from crudik.application.mentoring_request.send import SendMentoringByStudent, SendMentoringByUserRequest
from crudik.presentation.http_endpoints.error_model import ErrorModel

router = APIRouter(
    prefix="/student/request",
    tags=["Заявки студента на ментерство"],
    route_class=DishkaRoute,
)
security = HTTPBearer(auto_error=False)


@router.post(
    "",
    description="Создание заявки на ментерство студентом",
    responses={
        200: {
            "description": "Успешное получение данных",
        },
        404: {
            "description": "Ментор не найден",
            "model": ErrorModel,
        },
        401: {
            "description": "Студент не авторизован",
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


@router.get(
    "",
    description="Получение всех отправленных запросов на ментерство студента",
    responses={
        200: {
            "model": list[MentoringRequestData],
            "description": "Успешное получение данных",
        },
        401: {
            "description": "Студент не авторизован",
            "model": ErrorModel,
        },
    },
)
async def get_all_requests(
    interactor: FromDishka[ReadStudentMentoringRequests],
    _token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> list[MentoringRequestData]:
    return await interactor.execute()


@router.delete(
    "/{mentoring_request_id}",
    description="Получение всех отправленных запросов на ментерство студента",
    status_code=200,
    responses={
        200: {
            "description": "Запрос на ментерство удален",
        },
        401: {
            "description": "Студент не авторизован",
            "model": ErrorModel,
        },
        403: {
            "description": "Студент не может удалить запрос на ментерство",
            "model": ErrorModel,
        },
    },
)
async def delete_request(
    interactor: FromDishka[DeleteMentoringRequestById],
    mentoring_request_id: Annotated[UUID, Path(description="Идентификатор запроса на менторинг")],
    _token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> None:
    return await interactor.execute(mentoring_request_id)
