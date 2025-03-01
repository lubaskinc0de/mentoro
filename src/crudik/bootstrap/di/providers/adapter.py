from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from redis.asyncio import Redis

from crudik.adapters.config import RedisConfig
from crudik.adapters.file_manager import MinioFileManager
from crudik.adapters.redis import RedisStorage
from crudik.adapters.token_encoder import TokenEncoder


class AdapterProvider(Provider):
    redis_storage = provide(RedisStorage, scope=Scope.APP)
    file_manager = provide(MinioFileManager, scope=Scope.APP)
    encoder = provide(TokenEncoder, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def redis_client(self, config: RedisConfig) -> AsyncIterable[Redis]:
        redis = Redis(
            host=config.host,
            port=config.port,
            db=config.database,
        )
        yield redis
        await redis.aclose()
