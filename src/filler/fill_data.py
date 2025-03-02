import os

import aiohttp
from aiohttp import ClientSession

from crudik.adapters.test_api_gateway import TestApiGateway

INTERESTS = [
    "математика",
    "русский язык",
    "английский язык",
    "немецкий язык",
    "обществознание",
    "программирование",
    "python",
    "java",
    "sql",
    "devops",
    "mobile",
    "ci/cd",
    "матанализ",
    "теорвер",
    "чистая архитектура",
    "embed",
]

base_names = ["Name"]


async def fill_mentors(gateway: TestApiGateway) -> None: ...


async def fill_students(gateway: TestApiGateway) -> None: ...


async def fill_data() -> None:
    async with ClientSession(
        base_url=os.environ["EXTERNAL_API_URL"],
        connector=aiohttp.TCPConnector(ssl=False),
    ) as session:
        gateway = TestApiGateway(session)
        await fill_mentors(gateway)
        await fill_students(gateway)
