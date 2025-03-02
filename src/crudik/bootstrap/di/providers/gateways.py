from dishka import Provider, Scope, WithParents, provide_all

from crudik.adapters.gateway.access_token import AccessTokenGatewayImpl
from crudik.adapters.gateway.mentor import MentorContactGatewayImpl, MentorGatewayImpl, MentorSkillGatewayImpl
from crudik.adapters.gateway.mentoring_request import MentoringRequestGatewayImpl
from crudik.adapters.gateway.review import ReviewGatewayImpl
from crudik.adapters.gateway.student import StudentGatewayImpl
from crudik.adapters.gateway.swiped_gateway import SwipedMentorGatewayImpl


class GatewayProvider(Provider):
    scope = Scope.REQUEST

    provides = provide_all(
        WithParents[AccessTokenGatewayImpl],  # type: ignore[misc]
        WithParents[StudentGatewayImpl],  # type: ignore[misc]
        WithParents[MentorGatewayImpl],  # type: ignore[misc]
        WithParents[SwipedMentorGatewayImpl],  # type: ignore[misc]
        WithParents[MentorSkillGatewayImpl],  # type: ignore[misc]
        WithParents[MentorContactGatewayImpl],  # type: ignore[misc]
        WithParents[MentoringRequestGatewayImpl],  # type: ignore[misc]
        WithParents[ReviewGatewayImpl],  # type: ignore[misc]
    )
