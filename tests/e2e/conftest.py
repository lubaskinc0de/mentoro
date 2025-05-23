import os
from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass

import pytest
from aiohttp import ClientSession
from dishka import AsyncContainer
from redis.asyncio import Redis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from crudik.adapters.config import Config
from crudik.adapters.test_api_gateway import TestApiGateway
from crudik.application.data_model.mentor import MentorContactModel
from crudik.application.data_model.token_data import TokenResponse
from crudik.application.mentor.sign_up import SignUpMentorRequest
from crudik.application.student.sign_up import SignUpStudentRequest
from crudik.bootstrap.di.container import get_async_container


@dataclass(slots=True)
class CreatedStudent:
    student: SignUpStudentRequest
    token: TokenResponse


@dataclass(slots=True)
class CreatedMentor:
    mentor: SignUpMentorRequest
    token: TokenResponse


@pytest.fixture
def config() -> Config:
    return Config.load_from_environment()


@pytest.fixture
async def container(config: Config) -> AsyncIterator[AsyncContainer]:
    container = get_async_container(config)
    yield container
    await container.close()


@pytest.fixture
async def session(container: AsyncContainer) -> AsyncIterator[AsyncSession]:
    async with container() as r:
        yield (await r.get(AsyncSession))


@pytest.fixture
async def redis(container: AsyncContainer) -> Redis:
    return await container.get(Redis)


@pytest.fixture(autouse=True)
async def gracefully_teardown(
    session: AsyncSession,
) -> AsyncIterable[None]:
    yield
    await session.execute(
        text("""
            DO $$
            DECLARE
                tb text;
            BEGIN
                FOR tb IN (
                    SELECT tablename
                    FROM pg_catalog.pg_tables
                    WHERE schemaname = 'public'
                      AND tablename != 'alembic_version'
                )
                LOOP
                    EXECUTE 'TRUNCATE TABLE ' || tb || ' CASCADE';
                END LOOP;
            END $$;
        """),
    )
    await session.commit()


@pytest.fixture(scope="session")
def api_url() -> str:
    return os.environ["API_URL"]


@pytest.fixture
async def http_session(api_url: str) -> AsyncIterator[ClientSession]:
    async with ClientSession(base_url=api_url) as session:
        yield session


@pytest.fixture
async def api_gateway(http_session: ClientSession) -> TestApiGateway:
    return TestApiGateway(http_session)


@pytest.fixture
async def created_student(api_gateway: TestApiGateway) -> CreatedStudent:
    student = SignUpStudentRequest(full_name="Vasiliy Skilled", age=32, interests=["skills", "freebsd"])
    response = await api_gateway.sign_up_student(student)

    assert response.status_code == 200
    assert response.model is not None

    return CreatedStudent(
        student=student,
        token=response.model,
    )


@pytest.fixture
async def created_mentor(api_gateway: TestApiGateway) -> CreatedMentor:
    mentor = SignUpMentorRequest(
        full_name="Vasiliy Skilled",
        description="Vasiliy Skilled description",
        contacts=[MentorContactModel(url="ababyiExperienced", social_network="telegram")],
        skills=["expierence", "freebsd", "english"],
    )
    response = await api_gateway.sign_up_mentor(mentor)

    assert response.status_code == 200
    assert response.model is not None

    return CreatedMentor(
        mentor=mentor,
        token=response.model,
    )
