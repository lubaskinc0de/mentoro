from dataclasses import dataclass
from typing import BinaryIO

from pydantic import BaseModel, Field, HttpUrl

from crudik.adapters.file_manager import MinioFileManager
from crudik.adapters.idp import TokenStudentIdProvider, UnauthorizedError
from crudik.application.common.uow import UoW
from crudik.application.gateway.student_gateway import StudentGateway


class StudentAvatarData(BaseModel):
    avatar_url: HttpUrl = Field(description="Ссылка на аватарку студента")


@dataclass(slots=True, frozen=True)
class AttachAvatarToStudent:
    student_gateway: StudentGateway
    uow: UoW
    idp: TokenStudentIdProvider
    file_manager: MinioFileManager

    async def execute(
        self,
        file: BinaryIO,
        ext: str,
        size: int,
    ) -> StudentAvatarData:
        student = await self.student_gateway.get_by_id(await self.idp.get_student_id())
        if student is None:
            raise UnauthorizedError

        file_path = await self.file_manager.upload(file, ext, size)
        student.avatar_url = file_path

        await self.uow.commit()
        return StudentAvatarData(
            avatar_url=HttpUrl(file_path),
        )
