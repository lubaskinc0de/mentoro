from abc import abstractmethod
from typing import Protocol


class UoW(Protocol):
    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def add(self, instance: object) -> None: ...
