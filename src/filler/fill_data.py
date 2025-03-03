import asyncio
import os
import random
from io import BytesIO
from pathlib import Path

import aiohttp
from aiohttp import ClientSession
from faker import Faker

from crudik.adapters.test_api_gateway import TestApiGateway
from crudik.application.data_model.mentor import MentorContactModel
from crudik.application.mentor.sign_up import SignUpMentorRequest
from crudik.application.student.sign_up import SignUpStudentRequest

fake = Faker("ru_RU")

INTERESTS = [
    "Математика",
    "Английский язык",
    "Программирование",
    "Python",
    "Java",
    "Sql",
    "Devops",
    "Mobile",
    "Ci/cd",
    "Высшая Математика",
    "ML",
    "Data Science",
    "Embedded",
    "ML/Ops",
    "System Design",
]


async def fetch_random_image() -> bytes:
    base_path = Path("./src/filler/images")
    files = os.listdir(base_path)

    with (base_path / random.choice(files)).open("rb") as f:  # noqa: S311
        return f.read()


async def create_mentor(data: SignUpMentorRequest, gateway: TestApiGateway) -> None:
    resp = await gateway.sign_up_mentor(data)
    print(f"Status: {resp.status_code}; Created mentor: {data.full_name}")  # noqa: T201

    if resp.status_code == 409:
        print("Collision occured")  # noqa: T201
        return

    assert resp.model is not None
    resp_attach = await gateway.mentor_update_avatar(resp.model.access_token, BytesIO(await fetch_random_image()))
    if resp_attach.status_code != 200:
        print(f"While loading image: {resp_attach.status_code} {resp_attach.text}")  # noqa: T201


async def fill_mentors(gateway: TestApiGateway) -> None:
    mentors = [
        SignUpMentorRequest(
            full_name=f"{fake.first_name()} {fake.last_name()}",
            description="\n".join(fake.sentences(10)),
            contacts=[
                MentorContactModel(
                    social_network="Telegram",
                    url="https://t.me/lubaskinc0de",
                ),
            ],
            skills=[random.choice(INTERESTS) for _ in range(random.randint(1, len(INTERESTS)))],  # noqa: S311
        )
        for _ in range(100)
    ]
    req = [create_mentor(mentor_data, gateway) for mentor_data in mentors]
    await asyncio.gather(*req)


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


async def fill_history_students(gateway: TestApiGateway) -> None: ...


async def fill_data() -> None:
    async with ClientSession(
        base_url=os.environ["EXTERNAL_API_URL"],
        connector=aiohttp.TCPConnector(ssl=bool(int(os.environ.get("USE_SSL", False)))),
    ) as session:
        gateway = TestApiGateway(session)
        await fill_mentors(gateway)
        await fill_students(gateway)
        print("Done.")  # noqa: T201
