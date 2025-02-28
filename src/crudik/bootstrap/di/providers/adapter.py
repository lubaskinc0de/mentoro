from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from redis.asyncio import Redis

from crudik.adapters.config import RedisConfig
from crudik.adapters.redis import RedisStorage


class AdapterProvider(Provider):
    redis_storage = provide(RedisStorage, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def redis_client(self, config: RedisConfig) -> AsyncIterable[Redis]:
        redis = Redis(
            host=config.host,
            port=config.port,
            db=config.database,
        )
        yield redis
        await redis.aclose()
