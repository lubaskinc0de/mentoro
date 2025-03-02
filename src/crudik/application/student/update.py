from dataclasses import dataclass
from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints

from crudik.adapters.idp import TokenStudentIdProvider, UnauthorizedError
from crudik.application.common.uow import UoW
from crudik.application.gateway.student_gateway import StudentGateway


class UpdateStudentRequest(BaseModel):
    age: int | None = Field(ge=0, le=120, default=None, description="Student age")
    interests: list[Annotated[str, StringConstraints(min_length=2, max_length=30)]] | None = Field(
        min_length=1,
        max_length=100,
        default=None,
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
            raise UnauthorizedError

        if request.age:
            student.age = request.age
        if request.interests:
            student.interests = request.interests

        await self.uow.commit()
