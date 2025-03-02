from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crudik.application.review.common import ReviewGateway
from crudik.models.mentor import MentorReview


class ReviewGatewayImpl(ReviewGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_review(self, review_id: UUID) -> MentorReview | None:
        q = select(MentorReview).where(MentorReview.review_id == review_id)
        res = await self._session.execute(q)
        return res.scalar_one_or_none()
