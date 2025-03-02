from typing import Annotated
from uuid import UUID

import filetype  # type: ignore
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, Path, UploadFile
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from crudik.application.data_model.mentor import MentorData
from crudik.application.data_model.token_data import TokenResponse
from crudik.application.mentor.attach_avatar import AttachAvatarToMentor, MentorAvatarData
from crudik.application.mentor.read import ReadMentor
from crudik.application.mentor.read_by_id import ReadMentorById
from crudik.application.mentor.sign_in import SignInMentor, SignInMentorRequest
from crudik.application.mentor.sign_up import SignUpMentor, SignUpMentorRequest
from crudik.application.mentor.update import UpdateMentor, UpdateMentorRequest
from crudik.presentation.http_endpoints.error_model import ErrorModel
from crudik.presentation.http_endpoints.student import (
    CannotReadFileInfoError,
    CannotReadFileSizeError,
    FileIsNotImageError,
    FileTooBigError,
)

router = APIRouter(
    route_class=DishkaRoute,
    tags=["Ментор"],
    prefix="/mentor",
)

security = HTTPBearer(auto_error=False)
MAX_FILE_SIZE = 8 * 1024 * 1024


@router.post(
    "/sign_up",
    description="Авторизация ментора",
)
async def sign_up_mentor(
    schema: SignUpMentorRequest,
    interactor: FromDishka[SignUpMentor],
) -> TokenResponse:
    """Mentor registration."""
    return await interactor.execute(schema)


@router.post(
    "/sign_in",
    description="Регистрация ментора",
    responses={
        401: {
            "description": "Ментор не авторизован",
            "model": ErrorModel,
        },
    },
)
async def sign_in_mentor(
    schema: SignInMentorRequest,
    interactor: FromDishka[SignInMentor],
) -> TokenResponse:
    """Mentor login."""
    return await interactor.execute(schema)


@router.get(
    "/me",
    description="Получение данных ментора по токену",
    responses={
        401: {
            "description": "Ментор не авторизован",
            "model": ErrorModel,
        },
    },
)
async def read_mentor(
    command: FromDishka[ReadMentor],
    _token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> MentorData:
    """Read authorized mentor."""
    return await command.execute()


@router.put(
    "/attach",
    description="Загрузка фотографии ментора",
    responses={
        200: {
            "description": "Фотография успешно обновлена",
        },
        400: {
            "description": "Файл имеет неверный тип",
            "model": ErrorModel,
        },
        401: {
            "description": "Ментор не авторизован",
            "model": ErrorModel,
        },
        413: {
            "description": "Файл слишком большой",
            "model": ErrorModel,
        },
    },
)
async def attach_avatar(
    command: FromDishka[AttachAvatarToMentor],
    file: UploadFile,
    _token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> MentorAvatarData:
    """Attach avatar for mentor."""
    if not file.size:
        raise CannotReadFileSizeError

    if file.size > MAX_FILE_SIZE:
        raise FileTooBigError

    file_info = filetype.guess(await file.read(128))
    if file_info is None:
        raise CannotReadFileInfoError

    mime, ext = file_info.mime, file_info.extension

    if not mime.startswith("image/"):
        raise FileIsNotImageError

    return await command.execute(
        file.file,
        ext,
        file.size,
    )


@router.put(
    "/",
    description="Обновление данных ментора",
    responses={
        401: {
            "description": "Ментор не авторизован",
            "model": ErrorModel,
        },
    },
)
async def update_mentor(
    request: UpdateMentorRequest,
    interactor: FromDishka[UpdateMentor],
    _token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> None:
    """Update authorized mentor."""
    await interactor.execute(request)


@router.get(
    "/{mentor_id}",
    description="Получение данных ментора по идентификатору ментора",
    responses={
        404: {
            "description": "Не найден ментор",
            "model": ErrorModel,
        },
        401: {
            "description": "Ментор не авторизован",
            "model": ErrorModel,
        },
    },
)
async def read_mentor_by_id(
    command: FromDishka[ReadMentorById],
    mentor_id: Annotated[UUID, Path(description="Идентификатор ментора")],
    _token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> MentorData:
    """Read mentor by id (need student auth)."""
    return await command.execute(mentor_id)
