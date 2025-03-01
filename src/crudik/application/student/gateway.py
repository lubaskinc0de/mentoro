from abc import abstractmethod
from typing import Protocol

from crudik.models.student import Student


class StudentGateway(Protocol):
    @abstractmethod
    async def add(self, entity: Student) -> None:
        raise NotImplementedError
