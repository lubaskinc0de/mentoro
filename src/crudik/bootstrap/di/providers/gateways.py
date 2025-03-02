from dishka import Provider, Scope, WithParents, provide_all

from crudik.adapters.db.access_token import AccessTokenGatewayImpl
from crudik.adapters.db.mentor import MentorGatewayImpl
from crudik.adapters.db.student import StudentGatewayImpl
from crudik.adapters.db.swiped_gateway import SwipedMentorGatewayImpl


class GatewayProvider(Provider):
    scope = Scope.REQUEST

    provides = provide_all(
        WithParents[AccessTokenGatewayImpl],  # type: ignore[misc]
        WithParents[StudentGatewayImpl],  # type: ignore[misc]
        WithParents[MentorGatewayImpl],  # type: ignore[misc]
        WithParents[SwipedMentorGatewayImpl],  # type: ignore[misc]
    )
