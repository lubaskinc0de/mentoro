from dataclasses import dataclass

from crudik.adapters.idp import TokenStudentIdProvider, UnauthorizedError
from crudik.application.data_model.student import StudentData, convert_student_model_to_dto
from crudik.application.gateway.student_gateway import StudentGateway


@dataclass(slots=True, frozen=True)
class ReadStudent:
    student_gateway: StudentGateway
    idp: TokenStudentIdProvider

    async def execute(self) -> StudentData:
        student = await self.student_gateway.get_by_id(await self.idp.get_student_id())
        if student is None:
            raise UnauthorizedError

        return convert_student_model_to_dto(student)
