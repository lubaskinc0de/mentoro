from abc import abstractmethod
from typing import Protocol

from crudik.models.access_token import AccessToken


class AccessTokenGateway(Protocol):
    @abstractmethod
    async def add(self, entity: AccessToken) -> None:
        raise NotImplementedError
