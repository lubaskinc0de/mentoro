from typing import Annotated

import filetype  # type: ignore[import-untyped]
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, UploadFile
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from crudik.application.common.errors import ApplicationError
from crudik.application.data_model.mentor import MentorData
from crudik.application.data_model.student import StudentData
from crudik.application.data_model.token_data import TokenResponse
from crudik.application.mentor.interactors.update import UpdateMentor, UpdateMentorRequest
from crudik.application.student.interactors.attach_avatar import AttachAvatarToStudent, StudentAvatarData
from crudik.application.student.interactors.find_mentor import FindMentor
from crudik.application.student.interactors.read_student import ReadStudent
from crudik.application.student.interactors.sign_in import SignInStudent, SignInStudentRequest
from crudik.application.student.interactors.sign_up import SignUpStudent, SignUpStudentRequest
from crudik.application.student.interactors.swipe_mentor import SwipeMentor, SwipeMentorRequest
from crudik.application.student.interactors.update import UpdateStudent, UpdateStudentRequest
from crudik.presentation.http_endpoints.error_model import ErrorModel

router = APIRouter(
    route_class=DishkaRoute,
    tags=["Student"],
    prefix="/student",
)
MAX_FILE_SIZE = 20 * 1024 * 1024


class FileIsNotImageError(ApplicationError): ...


class FileTooBigError(ApplicationError): ...


class CannotReadFileSizeError(ApplicationError): ...


class CannotReadFileInfoError(ApplicationError): ...


security = HTTPBearer(auto_error=False)


@router.post("/sign_up")
async def sign_up_student(
    schema: SignUpStudentRequest,
    interactor: FromDishka[SignUpStudent],
) -> TokenResponse:
    """Student registration."""
    return await interactor.execute(schema)


@router.post(
    "/sign_in",
    responses={
        404: {
            "description": "Student not found",
            "model": ErrorModel,
        },
    },
)
async def sign_in_student(
    schema: SignInStudentRequest,
    interactor: FromDishka[SignInStudent],
) -> TokenResponse:
    """Student athorisation."""
    return await interactor.execute(schema)


@router.put(
    "/attach",
    responses={
        404: {
            "description": "Student not found",
            "model": ErrorModel,
        },
        401: {
            "description": "Unauthorized",
            "model": ErrorModel,
        },
    },
)
async def attach_avatar(
    command: FromDishka[AttachAvatarToStudent],
    file: UploadFile,
    _token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> StudentAvatarData:
    """Attach avatar for student."""
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
    responses={
        404: {
            "description": "Student not found",
            "model": ErrorModel,
        },
    },
)
async def update_student(
    request: UpdateStudentRequest,
    interactor: FromDishka[UpdateStudent],
) -> None:
    await interactor.execute(request)


@router.get(
    "/me",
    responses={
        404: {
            "description": "Student not found",
            "model": ErrorModel,
        },
        401: {
            "description": "Unauthorized",
            "model": ErrorModel,
        },
    },
)
async def read_student(
    command: FromDishka[ReadStudent],
    _token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> StudentData:
    return await command.execute()


@router.get(
    "/find",
    responses={
        404: {
            "description": "Student not found",
            "model": ErrorModel,
        },
        401: {
            "description": "Unauthorized",
            "model": ErrorModel,
        },
    },
)
async def find_mentor_for_student(
    command: FromDishka[FindMentor],
    _token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> MentorData | None:
    return await command.execute()


@router.post(
    "/swipe_mentor",
    responses={
        404: {
            "description": "Student not found",
            "model": ErrorModel,
        },
        401: {
            "description": "Unauthorized",
        },
    },
)
async def swipe_mentor(
    schema: SwipeMentorRequest,
    interactor: FromDishka[SwipeMentor],
) -> None:
    await interactor.execute(schema)


@router.put(
    "/",
    responses={
        404: {
            "description": "Mentor not found",
            "model": ErrorModel,
        },
    },
)
async def update_mentor(
    request: UpdateMentorRequest,
    interactor: FromDishka[UpdateMentor],
) -> None:
    await interactor.execute(request)
