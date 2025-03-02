from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from crudik.application.errors.common import ApplicationError
from crudik.presentation.http_endpoints.error_info import error_code, error_unique_code
from crudik.presentation.http_endpoints.mentor import router as mentor_router
from crudik.presentation.http_endpoints.mentoring_request import (
    mentor_router as mentoring_request_mentor_router,
)
from crudik.presentation.http_endpoints.mentoring_request import (
    student_router as mentoring_request_student_router,
)
from crudik.presentation.http_endpoints.reviews import router as review_router
from crudik.presentation.http_endpoints.root import router as root_router
from crudik.presentation.http_endpoints.student import router as student_router


def get_http_error_response(
    err: ApplicationError,
) -> JSONResponse:
    err_type = type(err)
    err_http_code = error_code[err_type]

    return JSONResponse(
        status_code=err_http_code,
        content={
            "code": error_unique_code[err_type],
        },
    )


async def app_exception_handler(_request: Request, exc: ApplicationError) -> JSONResponse:
    return get_http_error_response(exc)


async def unique_exception_handler(_request: Request, _exc: IntegrityError) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"code": "CONFLICT_ERROR"},
    )


async def validation_exception_handler(_request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body, "code": "VALIDATION_ERROR"}),
    )


def include_routers(app: FastAPI) -> None:
    app.include_router(root_router)
    app.include_router(mentoring_request_student_router)
    app.include_router(student_router)
    app.include_router(mentoring_request_mentor_router)
    app.include_router(mentor_router)
    app.include_router(review_router)


def include_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ApplicationError, app_exception_handler)  # type: ignore
    app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore
    app.add_exception_handler(IntegrityError, unique_exception_handler)  # type: ignore
