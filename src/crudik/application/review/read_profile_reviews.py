from dataclasses import dataclass

from crudik.adapters.idp import TokenMentorIdProvider, UnauthorizedError
from crudik.application.data_model.review import ReviewFullData, convert_full_reviews_to_dto
from crudik.application.gateway.mentor_gateway import MentorGateway
from crudik.application.gateway.review_gateway import ReviewGateway


@dataclass(slots=True, frozen=True)
class ReadMentorProfileReviews:
    gateway: MentorGateway
    idp: TokenMentorIdProvider
    review_gateway: ReviewGateway
    mentor_gateway: MentorGateway

    async def execute(self) -> list[ReviewFullData]:
        mentor = await self.mentor_gateway.get_by_id(await self.idp.get_mentor_id())
        if mentor is None:
            raise UnauthorizedError

        reviews: list[ReviewFullData] = convert_full_reviews_to_dto(
            await self.review_gateway.get_mentor_reviews(mentor.id)
        )
        return reviews
