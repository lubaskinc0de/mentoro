from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from crudik.models.mentoring_request import MentoringRequest


class MentoringRequestGateway(Protocol):
    @abstractmethod
    async def read_all_by_student(self, student_id: UUID) -> list[MentoringRequest]:
        raise NotImplementedError

    @abstractmethod
    async def read_all_by_mentor(self, mentor_id: UUID) -> list[MentoringRequest]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, unique_id: UUID) -> MentoringRequest | None:
        raise NotImplementedError
