from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import FastapiProvider

from crudik.adapters.config import Config, FilesConfig, PostgresqlConfig, RedisConfig
from crudik.bootstrap.di.providers.adapter import AdapterProvider
from crudik.bootstrap.di.providers.command import CommandProvider
from crudik.bootstrap.di.providers.config import ConfigProvider
from crudik.bootstrap.di.providers.connection import ConnectionProvider


def get_async_container(
    config: Config,
) -> AsyncContainer:
    container = make_async_container(
        ConfigProvider(),
        FastapiProvider(),
        AdapterProvider(),
        CommandProvider(),
        ConnectionProvider(),
        context={
            RedisConfig: config.redis,
            PostgresqlConfig: config.postgresql,
            FilesConfig: config.files,
        },
    )
    return container
