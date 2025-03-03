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


def get_image(file_name: str) -> bytes:
    with Path(file_name).open("rb") as f:
        return f.read()


MENTOR_IMAGES = [
    "src/filler/images/0bed979a-b777-4ef2-bb16-3635eaaf1760.jpg",
    "src/filler/images/00d7811d-d478-4d5c-aeb5-f6f8d7ee84eb.jpg",
    "src/filler/images/0d387054-9ed2-4b66-a038-7ada95962bc0.jpg",
    "src/filler/images/1d8c8e97-2e93-464e-b8bf-4ada30997e68.jpg",
    "src/filler/images/f5d72ffe-bbcd-44e8-8247-b71bcc5e2120.jpg",
]

STUDENT_IMAGES = [
    "src/filler/images/f5d72ffe-bbcd-44e8-8247-b71bcc5e2120.jpg",
    "src/filler/images/e47c7520-8150-42ea-ba93-65aec3075521.jpg",
    "src/filler/images/dd4a4df5-d687-4e96-b507-d358ddb3379c.jpg",
    "src/filler/images/db790f53-35d7-4c35-8bc4-60848100eefc.jpg",
    "src/filler/images/2bac0731-4aa8-47ea-8fa5-f7b2e9d06d8b.jpg",
]


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
    names = ["Опытный Василий", "Владислав IT", "Ярослав Python", "Михаил JS", "Даня React"]
    mentors = [
        SignUpMentorRequest(
            full_name=f"{name}",
            description="\n".join(fake.sentences(10)),
            contacts=[
                MentorContactModel(
                    social_network="Telegram",
                    url="https://t.me/lubaskinc0de",
                ),
            ],
            skills=[random.choice(INTERESTS) for _ in range(random.randint(1, len(INTERESTS)))],  # noqa: S311
        )
        for name in names
    ]
    req = [
        create_mentor(mentor_data, gateway, get_image(image))
        for mentor_data, image in zip(mentors, MENTOR_IMAGES, strict=True)
    ]
    await asyncio.gather(*req)


async def fill_students(gateway: TestApiGateway) -> None:
    names = ["Майкл", "Влад", "Илья", "Иван", "Максим"]
    for name, image in zip(names, STUDENT_IMAGES, strict=True):
        request = SignUpStudentRequest(
            full_name=f"Студент {name}",
            age=random.randint(15, 25),  # noqa: S311
            interests=[random.choice(INTERESTS) for _ in range(random.randint(1, 6))],  # noqa: S311
        )
        resp = await gateway.sign_up_student(request)
        if resp.status_code == 409:
            print("Student already created")  # noqa: T201
        elif resp.status_code != 200:
            msg = f"Cannot create student {resp.text}"
            raise ValueError(msg)
        assert resp.model is not None
        await gateway.student_update_avatar(resp.model.access_token, BytesIO(get_image(image)))


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
