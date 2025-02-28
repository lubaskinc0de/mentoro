from dishka import Provider, Scope, from_context

from crudik.adapters.config import PostgresqlConfig, RedisConfig


class ConfigProvider(Provider):
    scope = Scope.APP

    configs = from_context(RedisConfig) + from_context(PostgresqlConfig)
