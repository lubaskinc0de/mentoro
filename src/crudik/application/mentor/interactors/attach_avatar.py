from dataclasses import dataclass
from typing import BinaryIO

from pydantic import BaseModel, Field, HttpUrl

from crudik.adapters.file_manager import MinioFileManager
from crudik.adapters.idp import TokenMentorIdProvider, UnauthorizedError
from crudik.application.mentor.gateway import MentorGateway
from crudik.application.uow import UoW


class MentorAvatarData(BaseModel):
    photo_url: HttpUrl = Field(description="Mentor avatar url")


@dataclass(slots=True, frozen=True)
class AttachAvatarToMentor:
    mentor_gateway: MentorGateway
    uow: UoW
    idp: TokenMentorIdProvider
    file_manager: MinioFileManager

    async def execute(
        self,
        file: BinaryIO,
        ext: str,
        size: int,
    ) -> MentorAvatarData:
        mentor = await self.mentor_gateway.get_by_id(await self.idp.get_mentor_id())
        if mentor is None:
            raise UnauthorizedError

        file_path = await self.file_manager.upload(file, ext, size)
        mentor.photo_url = file_path

        await self.uow.commit()
        return MentorAvatarData(
            photo_url=HttpUrl(file_path),
        )
