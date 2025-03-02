from dataclasses import dataclass

from crudik.adapters.idp import TokenStudentIdProvider, UnauthorizedError
from crudik.application.data_model.mentor import MentorData, convert_mentor_to_dto
from crudik.application.mentor.gateway import MentorGateway
from crudik.application.student.gateway import StudentGateway
from crudik.application.uow import UoW
from crudik.models.mentor import MatchHistory


@dataclass(slots=True, frozen=True)
class FindMentor:
    student_gateway: StudentGateway
    mentor_gateway: MentorGateway
    idp: TokenStudentIdProvider
    uow: UoW

    async def execute(self) -> MentorData | None:
        student = await self.student_gateway.get_by_id(await self.idp.get_student_id())
        if student is None:
            raise UnauthorizedError

        match = await self.mentor_gateway.get_match(student.id)
        if match is None:
            await self.mentor_gateway.clear_history(student.id)
            match = await self.mentor_gateway.get_match(student.id)

        if match is not None:
            if not await self.mentor_gateway.exists_in_history(student.id, match.id):
                history_record = MatchHistory(
                    student_id=student.id,
                    mentor_id=match.id,
                )
                self.uow.add(history_record)
                await self.uow.commit()
            return convert_mentor_to_dto(match)
        return None
