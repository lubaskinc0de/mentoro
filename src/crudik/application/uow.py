from abc import abstractmethod
from typing import Any, Protocol


class UoW(Protocol):
    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def add(self, instance: Any) -> None: ...

    @abstractmethod
    def add_all(self, instances: list[Any]) -> None: ...

    @abstractmethod
    def delete(self, instance: Any) -> None: ...
