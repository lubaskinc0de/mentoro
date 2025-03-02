from abc import abstractmethod
from collections.abc import Sequence
from typing import Protocol
from uuid import UUID

from crudik.models.mentor import Mentor


class MentorGateway(Protocol):
    @abstractmethod
    async def get_by_id(self, unique_id: UUID) -> Mentor | None: ...

    @abstractmethod
    async def get_by_name(self, name: str) -> Mentor | None: ...

    @abstractmethod
    async def get_match(self, student_id: UUID, threshold: float = 0.45) -> Sequence[Mentor]: ...

    @abstractmethod
    async def clear_history(self, student_id: UUID) -> None: ...

    @abstractmethod
    async def exists_in_history(self, student_id: UUID, mentor_id: UUID) -> bool: ...
