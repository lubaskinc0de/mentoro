from pydantic import BaseModel


class ErrorResponse(BaseModel):
    error: str

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from crudik.application.common.errors import ApplicationError
from crudik.presentation.http_endpoints.root import router as root_router

error_code = {
    ApplicationError: 500,
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


def include_routers(app: FastAPI) -> None:
    app.include_router(root_router)


def include_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ApplicationError, app_exception_handler)  # type: ignore
