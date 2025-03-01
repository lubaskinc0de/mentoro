import os
import random

import aiohttp
from aiohttp import ClientSession

from crudik.application.mentor.interactors.sign_up import SignUpMentorRequest
from filler.test_gateway import TestApiGateway

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


async def fill_mentors(gateway: TestApiGateway) -> None:
    mentors = [
        "Опытный Василий IT",
        "Илья Любавский",
        "Илья Горюнов",
        "Иван Кирпичников",
        "Максим Светличный",
        "Владислав Смирнов",
    ]
    mentors_objs = [
        SignUpMentorRequest(
            full_name=name,
            age=random.randint(15, 20),  # noqa: S311
            skills=[random.choice(INTERESTS) for _ in range(1, 4)],  # noqa: S311
            contacts=["https://t.me/lubaskinc0de"],
        )
        for name in mentors
    ]

    for mentor in mentors_objs:
        response = await gateway.sign_up_mentor(mentor)
        assert response.status_code == 200


async def fill_students(gateway: TestApiGateway) -> None: ...


async def fill_data() -> None:
    async with ClientSession(
        base_url=os.environ["EXTERNAL_API_URL"],
        connector=aiohttp.TCPConnector(ssl=False),
    ) as session:
        gateway = TestApiGateway(session)
        await fill_mentors(gateway)
        await fill_students(gateway)
