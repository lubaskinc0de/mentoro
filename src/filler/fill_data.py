import asyncio
import os
import random

from aiohttp import ClientSession

from crudik.application.mentor.interactors.sign_up import SignUpMentorRequest
from crudik.application.student.interactors.sign_up import SignUpStudentRequest
from tests.e2e.gateway import TestApiGateway

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
    students = [
        SignUpMentorRequest(
            full_name=name,
            age=random.randint(15, 20),  # noqa: S311
            skills=[random.choice(INTERESTS) for _ in range(1, 4)],  # noqa: S311
        )
        for name in base_names
    ]

    for student in students:
        await gateway.sign_up_student(student)


async def fill_mentors(gateway: TestApiGateway) -> None: ...


async def main() -> None:
    async with ClientSession(base_url=os.environ["EXTERNAL_API_URL"]) as session:
        gateway = TestApiGateway(session)
        await fill_students(gateway)


if __name__ == "__main__":
    asyncio.run(main())
