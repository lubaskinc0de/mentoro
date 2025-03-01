from collections.abc import AsyncIterator

import miniopy_async  # type:ignore[import-untyped]
from dishka import Provider, Scope, from_context, provide

from crudik.adapters.config import FilesConfig, PostgresqlConfig, RedisConfig


class ConfigProvider(Provider):
    scope = Scope.APP

    configs = from_context(RedisConfig) + from_context(PostgresqlConfig) + from_context(FilesConfig)

    @provide(scope=Scope.APP)
    async def minio_client(self, config: FilesConfig) -> AsyncIterator[miniopy_async.Minio]:
        client = miniopy_async.Minio(
            config.minio_url,
            access_key=config.minio_access_key,
            secret_key=config.minio_secret_key,
            secure=False,
        )
        yield client
