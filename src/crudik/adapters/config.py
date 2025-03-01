import os
from dataclasses import dataclass
from datetime import timedelta
from typing import Self


@dataclass(frozen=True, slots=True)
class ServerConfig:
    host: str
    port: int
    access_log: bool


@dataclass(frozen=True, slots=True)
class RedisConfig:
    host: str
    port: int
    database: int


@dataclass(frozen=True, slots=True)
class PostgresqlConfig:
    username: str
    password: str
    host: str
    port: int
    database: str

    @property
    def connection_url(self) -> str:
        return f"postgresql+asyncpg://{self.username}:{self.password}@{self.host}/{self.database}"


@dataclass(frozen=True, slots=True)
class FilesConfig:
    minio_access_key: str
    minio_secret_key: str
    minio_url: str
    file_server: str


@dataclass(frozen=True, slots=True)
class AccessTokenConfig:
    expires_in: timedelta


@dataclass(frozen=True, slots=True)
class Config:
    redis: RedisConfig
    server: ServerConfig
    postgresql: PostgresqlConfig
    files: FilesConfig
    access_token: AccessTokenConfig

    @classmethod
    def load_from_environment(cls) -> Self:
        return cls(
            redis=RedisConfig(
                host=os.environ["REDIS_HOST"],
                port=int(os.environ["REDIS_PORT"]),
                database=int(os.environ["REDIS_DATABASE"]),
            ),
            server=ServerConfig(
                host=os.environ["SERVER_HOST"],
                port=int(os.environ["SERVER_PORT"]),
                access_log=bool(int(os.environ["SERVER_ACCESS_LOG"])),
            ),
            postgresql=PostgresqlConfig(
                username=os.environ["POSTGRES_USERNAME"],
                password=os.environ["POSTGRES_PASSWORD"],
                host=os.environ["POSTGRES_HOST"],
                port=int(os.environ["POSTGRES_PORT"]),
                database=os.environ["POSTGRES_DATABASE"],
            ),
            files=FilesConfig(
                minio_access_key=os.environ["MINIO_ACCESS_KEY"],
                minio_secret_key=os.environ["MINIO_SECRET_KEY"],
                minio_url=os.environ["MINIO_URL"],
                file_server=os.environ["FILE_SERVER_URL"],
            ),
            access_token=AccessTokenConfig(
                expires_in=timedelta(
                    minutes=int(
                        os.environ["ACCESS_TOKEN_EXPIRES_IN"],
                    ),
                ),
            ),
        )
