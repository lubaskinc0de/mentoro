from abc import abstractmethod
from typing import Protocol


class Commitable(Protocol):
    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError
