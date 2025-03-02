from abc import abstractmethod
from typing import Protocol
from uuid import UUID


class MentorSkillGateway(Protocol):
    @abstractmethod
    async def delete_by_mentor_id(self, mentod_id: UUID) -> None:
        raise NotImplementedError
