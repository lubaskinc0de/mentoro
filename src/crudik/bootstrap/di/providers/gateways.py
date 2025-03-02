from dishka import Provider, Scope, WithParents, provide_all

from crudik.adapters.db.access_token import AccessTokenGatewayImpl
from crudik.adapters.db.mentor import MentorContactGatewayImpl, MentorGatewayImpl, MentorSkillGatewayImpl
from crudik.adapters.db.student import StudentGatewayImpl
from crudik.adapters.db.swiped_gateway import SwipedMentorGatewayImpl
from crudik.adapters.db.mentoring_request import MentorignRequestGatewayImpl


class GatewayProvider(Provider):
    scope = Scope.REQUEST

    provides = provide_all(
        WithParents[AccessTokenGatewayImpl],  # type: ignore[misc]
        WithParents[StudentGatewayImpl],  # type: ignore[misc]
        WithParents[MentorGatewayImpl],  # type: ignore[misc]
        WithParents[SwipedMentorGatewayImpl],  # type: ignore[misc]
        WithParents[MentorSkillGatewayImpl],  # type: ignore[misc]
        WithParents[MentorContactGatewayImpl],  # type: ignore[misc]
        WithParents[MentorignRequestGatewayImpl],  # type: ignore[misc]
    )
