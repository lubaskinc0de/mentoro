from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from crudik.models.mentoring_request import MentoringRequest


class MentorignRequestGateway(Protocol):
    @abstractmethod
    async def read_all(self, student_id: UUID) -> list[MentoringRequest]:
        raise NotImplementedError
