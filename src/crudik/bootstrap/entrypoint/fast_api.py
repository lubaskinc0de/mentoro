import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from crudik.adapters.config import Config
from crudik.bootstrap.di.container import get_async_container
from crudik.presentation.http import include_exception_handlers, include_routers

log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console"],
    },
}


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield
    await app.state.dishka_container.close()


def run_api(_args: list[str]) -> None:
    app = FastAPI(
        lifespan=lifespan,
        root_path="/api",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )
    config = Config.load_from_environment()
    container = get_async_container(config)

    setup_dishka(container=container, app=app)

    logging.info("Fastapi app created.")

    include_routers(app)
    include_exception_handlers(app)

    uvicorn.run(
        app,
        port=config.server.port,
        host=config.server.host,
        log_config=log_config,
        access_log=config.server.access_log,
    )
