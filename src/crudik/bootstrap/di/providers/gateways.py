from dishka import Provider, Scope, WithParents, provide_all

from crudik.application.access_token.gateway import AccessTokenGateway
from crudik.application.student.gateway import StudentGateway


class GatewayProvider(Provider):
    scope = Scope.REQUEST

    provides = provide_all(
        WithParents[AccessTokenGateway],  # type: ignore[misc]
        WithParents[StudentGateway],  # type: ignore[misc]
    )
