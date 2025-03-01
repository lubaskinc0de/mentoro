from sqlalchemy.ext.asyncio import AsyncSession

from crudik.application.access_token.gateway import AccessTokenGateway


class AccessTokenGatewayImpl(AccessTokenGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
