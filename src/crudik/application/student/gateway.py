from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from crudik.models.student import Student


class StudentGateway(Protocol):
    @abstractmethod
    async def get_by_id(self, unique_id: UUID) -> Student | None: ...

    @abstractmethod
    async def get_by_name(self, name: str) -> Student | None: ...
