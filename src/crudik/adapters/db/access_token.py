from sqlalchemy.ext.asyncio import AsyncSession

from crudik.application.access_token.gateway import AccessTokenGateway
from crudik.models.access_token import AccessToken


class AccessTokenGatewayImpl(AccessTokenGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, entity: AccessToken) -> None:
        self._session.add(entity)
