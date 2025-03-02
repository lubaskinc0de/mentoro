from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from crudik.models.swiped_mentor import SwipedMentor, SwipedMentorType


class SwipedMentorGateway(Protocol):
    @abstractmethod
    async def get_all(
        self,
        student_id: UUID,
        swiped_mentor_type: SwipedMentorType,
    ) -> list[SwipedMentor]:
        raise NotImplementedError

    @abstractmethod
    async def read(self, student_id: UUID, mentor_id: UUID) -> SwipedMentor | None:
        raise NotImplementedError
