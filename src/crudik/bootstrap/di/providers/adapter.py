from collections.abc import AsyncIterable

from aiohttp import ClientSession
from dishka import Provider, Scope, from_context, provide, provide_all
from fastapi import Request
from redis.asyncio import Redis

from crudik.adapters.config import RedisConfig
from crudik.adapters.file_manager import MinioFileManager
from crudik.adapters.idp import TokenBearerParser, TokenMentorIdProvider, TokenStudentIdProvider
from crudik.adapters.redis import RedisStorage
from crudik.adapters.test_api_gateway import TestApiGateway
from crudik.adapters.token_encoder import TokenEncoder


class AdapterProvider(Provider):
    redis_storage = provide(RedisStorage, scope=Scope.APP)
    file_manager = provide(MinioFileManager, scope=Scope.APP)
    encoder = provide(TokenEncoder, scope=Scope.APP)
    request = from_context(Request, scope=Scope.REQUEST)
    token_bearer_parser = provide(TokenBearerParser, scope=Scope.REQUEST)
    idp = provide_all(TokenStudentIdProvider, TokenMentorIdProvider, scope=Scope.REQUEST)

    @provide(scope=Scope.APP)
    async def redis_client(self, config: RedisConfig) -> AsyncIterable[Redis]:
        redis = Redis(
            host=config.host,
            port=config.port,
            db=config.database,
        )
        yield redis
        await redis.aclose()

    @provide(scope=Scope.APP)
    async def api_gateway(self) -> AsyncIterable[TestApiGateway]:
        session = ClientSession("https://prod-team-6-a36eo8k0.final.prodcontest.ru/")
        yield TestApiGateway(session)
        await session.close()

