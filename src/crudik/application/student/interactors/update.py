from dataclasses import dataclass
from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints

from crudik.adapters.idp import TokenStudentIdProvider
from crudik.application.student.errors import StudentDoesNotExistsError
from crudik.application.student.gateway import StudentGateway
from crudik.application.uow import UoW


class UpdateStudentRequest(BaseModel):
    age: int = Field(ge=0, le=120, description="Student age")
    interests: list[Annotated[str, StringConstraints(min_length=2, max_length=30)]] = Field(
        min_length=1,
        max_length=100,
        description="Student interests",
    )


@dataclass(frozen=True, slots=True)
class UpdateStudent:
    uow: UoW
    student_gateway: StudentGateway
    student_id_provider: TokenStudentIdProvider

    async def execute(self, request: UpdateStudentRequest) -> None:
        student_id = await self.student_id_provider.get_student_id()
        student = await self.student_gateway.get_by_id(student_id)
        if student is None:
            raise StudentDoesNotExistsError

        student.age = request.age
        student.interests = request.interests

        await self.uow.commit()
