from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from crudik.application.common.errors import ApplicationError
from crudik.presentation.http_endpoints.root import router as root_router
from crudik.presentation.http_endpoints.student import router as student_router

error_code = {
    ApplicationError: 500,
}
error_unique_code = {
    ApplicationError: "APPLICATION_ERROR",
}


def get_http_error_response(
    err: ApplicationError,
) -> JSONResponse:
    err_type = type(err)
    err_http_code = error_code[err_type]

    return JSONResponse(
        status_code=err_http_code,
        content={},
    )


async def app_exception_handler(_request: Request, exc: ApplicationError) -> JSONResponse:
    return get_http_error_response(exc)


async def validation_exception_handler(_request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body, "code": "VALIDATION_ERROR"}),
    )


def include_routers(app: FastAPI) -> None:
    app.include_router(root_router)
    app.include_router(student_router)


def include_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ApplicationError, app_exception_handler)  # type: ignore
    app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore
