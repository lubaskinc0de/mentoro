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


def get_images() -> list[bytes]:
    base_path = Path("./src/filler/images")
    files = os.listdir(base_path)
    res = []
    for file in files:
        with (base_path / file).open("rb") as f:
            res.append(f.read())
    return res


async def create_mentor(data: SignUpMentorRequest, gateway: TestApiGateway, img: bytes) -> None:
    resp = await gateway.sign_up_mentor(data)
    print(f"Status: {resp.status_code}; Created mentor: {data.full_name}")  # noqa: T201

    if resp.status_code == 409:
        print("Collision occured")  # noqa: T201
        return

    assert resp.model is not None

    resp_attach = await gateway.mentor_update_avatar(resp.model.access_token, BytesIO(img))
    if resp_attach.status_code != 200:
        print(f"While loading image: {resp_attach.status_code} {resp_attach.text}")  # noqa: T201


async def fill_mentors(gateway: TestApiGateway) -> None:
    images = get_images()
    mentors = [
        SignUpMentorRequest(
            full_name=f"{fake.first_name()} ментор {x}",
            description="\n".join(fake.sentences(10)),
            contacts=[
                MentorContactModel(
                    social_network="Telegram",
                    url="https://t.me/lubaskinc0de",
                ),
            ],
            skills=[random.choice(INTERESTS) for _ in range(random.randint(1, len(INTERESTS)))],  # noqa: S311
        )
        for x in range(1, 6)
    ]
    req = [create_mentor(mentor_data, gateway, random.choice(images)) for mentor_data in mentors]  # noqa: S311
    await asyncio.gather(*req)


async def fill_students(gateway: TestApiGateway, n: int = 5) -> None:
    for x in range(1, n + 1):
        name = fake.name()
        request = SignUpStudentRequest(
            full_name=f"Студент {name} - {x}",
            age=random.randint(15, 25),  # noqa: S311
            interests=[random.choice(INTERESTS) for _ in range(random.randint(1, 6))],  # noqa: S311
        )
        resp = await gateway.sign_up_student(request)
        if resp.status_code == 409:
            print("Student already created")  # noqa: T201
        elif resp.status_code != 200:
            msg = f"Cannot create student {resp.text}"
            raise ValueError(msg)


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
