from dataclasses import dataclass
from typing import BinaryIO

from pydantic import BaseModel, Field, HttpUrl

from crudik.adapters.file_manager import MinioFileManager
from crudik.adapters.idp import TokenStudentIdProvider
from crudik.application.student.errors import StudentDoesNotExistsError
from crudik.application.student.gateway import StudentGateway
from crudik.application.uow import UoW


class StudentAvatarData(BaseModel):
    avatar_url: HttpUrl = Field(description="Student avatar url")


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
            raise StudentDoesNotExistsError

        file_path = await self.file_manager.upload(file, ext, size)
        student.avatar_url = file_path

        await self.uow.commit()
        return StudentAvatarData(
            avatar_url=HttpUrl(file_path),
        )
