from typing import Annotated

import filetype  # type: ignore
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, UploadFile
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from crudik.application.data_model.mentor import MentorData
from crudik.application.data_model.token_data import TokenResponse
from crudik.application.mentor.interactors.attach_avatar import AttachAvatarToMentor, MentorAvatarData
from crudik.application.mentor.interactors.read import ReadMentor
from crudik.application.mentor.interactors.sign_in import SignInMentor, SignInMentorRequest
from crudik.application.mentor.interactors.sign_up import SignUpMentor, SignUpMentorRequest
from crudik.presentation.http_endpoints.error_model import ErrorModel
from crudik.presentation.http_endpoints.student import (
    CannotReadFileInfoError,
    CannotReadFileSizeError,
    FileIsNotImageError,
    FileTooBigError,
)

router = APIRouter(
    route_class=DishkaRoute,
    tags=["Mentor"],
    prefix="/mentor",
)

security = HTTPBearer(auto_error=False)
MAX_FILE_SIZE = 20 * 1024 * 1024


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
            "description": "Mentor not found",
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


@router.get(
    "/me",
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
async def read_mentor(
    command: FromDishka[ReadMentor],
    _token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> MentorData:
    return await command.execute()


@router.put(
    "/attach",
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
