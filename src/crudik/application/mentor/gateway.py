from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from crudik.models.mentor import Mentor


class MentorGateway(Protocol):
    @abstractmethod
    async def get_by_id(self, unique_id: UUID) -> Mentor | None: ...

    @abstractmethod
    async def get_by_name(self, name: str) -> Mentor | None: ...
