import os
import random

import aiohttp
from aiohttp import ClientSession
from faker import Faker

from crudik.adapters.test_api_gateway import TestApiGateway
from crudik.application.data_model.mentor import MentorContactModel
from crudik.application.mentor.interactors.sign_up import SignUpMentorRequest
from crudik.application.student.interactors.sign_up import SignUpStudentRequest

fake = Faker("ru_RU")

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
    mentor_names = [
        "Опытный Василий IT",
        "Илья Любавский ОПЫТНЫЙ",
        "Илья Горюнов | Embed",
        "Иван Кирпичников IT",
        "Влад Смирнов | IT",
        "Максим Светличный | Mobile",
    ]
    mentor_descriptions = [
        "Опытный Василий IT. Спокойный и рассудительный, с отличным чувством юмора. \
        Любит объяснять сложные вещи простым языком. Обожает хайкинг и кофе.",
        "Илья Любавский. Энергичный и целеустремленный, всегда готов помочь. \
            Увлекается киберспортом и чтением научной фантастики. Немного перфекционист.",
        "Илья Горюнов. Уравновешенный и внимательный к деталям. Обожа\
            ет работать с железом и вдохновлять других. В свободное время занимается робототехникой.",
        "Иван Кирпичников. Добродушный и открытый, с широким кругозором\
            . Любит путешествовать и изучать новые технологии. Фанат настольных игр.",
        "Влад Смирнов. Харизматичный и общительный, с сильными лидерскими\
              качествами. Увлекается фотографией и автоспортом. Всегда готов к новым вызовам.",
        "Максим Светличный. Креативный и амбициозный, с любовью к мобильн\
            ым технологиям. В свободное время занимается дизайном и играет на гитаре.",
    ]
    mentors = [
        SignUpMentorRequest(
            full_name=name,
            description=description,
            contacts=[
                MentorContactModel(
                    social_network="Telegram",
                    url="https://t.me/lubaskinc0de",
                ),
            ],
            skills=[random.choice(INTERESTS) for _ in range(random.randint(1, 6))],  # noqa: S311
        )
        for name, description in zip(mentor_names, mentor_descriptions, strict=True)
    ]

    for mentor_data in mentors:
        resp = await gateway.sign_up_mentor(mentor_data)
        if resp.status_code == 409:
            print("Mentor already created")  # noqa: T201
        elif resp.status_code != 200:
            raise ValueError("Cannot create mentor")


async def fill_students(gateway: TestApiGateway, n: int = 10) -> None:
    for _ in range(n):
        name = fake.name()
        request = SignUpStudentRequest(
            full_name=name,
            age=random.randint(15, 25),  # noqa: S311
            interests=[random.choice(INTERESTS) for _ in range(random.randint(1, 6))],  # noqa: S311
        )
        resp = await gateway.sign_up_student(request)
        if resp.status_code == 409:
            print("Student already created")  # noqa: T201
        elif resp.status_code != 200:
            raise ValueError("Cannot create student")

    prod_student = SignUpStudentRequest(full_name="PROD", age=20, interests=INTERESTS, description="PRODDDDoooooDD")
    resp = await gateway.sign_up_student(prod_student)

async def fill_history_students(gateway: TestApiGateway) -> None:
    ...

async def fill_data() -> None:
    async with ClientSession(
        base_url=os.environ["EXTERNAL_API_URL"],
        connector=aiohttp.TCPConnector(ssl=bool(int(os.environ.get("USE_SSL", False)))),
    ) as session:
        gateway = TestApiGateway(session)
        await fill_mentors(gateway)
        await fill_students(gateway)
        print("Done.")  # noqa: T201
