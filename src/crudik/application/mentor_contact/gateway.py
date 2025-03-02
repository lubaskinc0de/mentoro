from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from crudik.models.mentor import MentorContact


class MentorContactGateway(Protocol):
    @abstractmethod
    async def get_by_id(self, unique_id: UUID) -> MentorContact | None:
        raise NotImplementedError

    @abstractmethod
    async def delete_by_mentor_id(self, mentod_id: UUID) -> None:
        raise NotImplementedError
