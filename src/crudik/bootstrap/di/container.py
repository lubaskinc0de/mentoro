from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import FastapiProvider

from crudik.adapters.config import Config, FilesConfig, PostgresqlConfig, RedisConfig, SecretConfig
from crudik.bootstrap.di.providers.adapter import AdapterProvider
from crudik.bootstrap.di.providers.config import ConfigProvider
from crudik.bootstrap.di.providers.connection import ConnectionProvider
from crudik.bootstrap.di.providers.gateways import GatewayProvider
from crudik.bootstrap.di.providers.interactors import InteractorsProvider


def get_async_container(
    config: Config,
) -> AsyncContainer:
    container = make_async_container(
        ConfigProvider(),
        FastapiProvider(),
        AdapterProvider(),
        GatewayProvider(),
        InteractorsProvider(),
        ConnectionProvider(),
        context={
            RedisConfig: config.redis,
            PostgresqlConfig: config.postgresql,
            FilesConfig: config.files,
            SecretConfig: config.secret,
        },
    )
    return container
