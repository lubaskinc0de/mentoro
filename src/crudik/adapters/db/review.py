from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from crudik.application.review.common import ReviewGateway
from crudik.models.mentor import Mentor, MentorReview


class ReviewGatewayImpl(ReviewGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_review(self, review_id: UUID) -> MentorReview | None:
        q = select(MentorReview).where(MentorReview.review_id == review_id)
        res = await self._session.execute(q)
        return res.scalar_one_or_none()

    async def get_mentor_reviews(self, mentor_id: UUID) -> Sequence[MentorReview]:
        q = (
            select(MentorReview)
            .where(MentorReview.mentor_id == mentor_id)
            .options(
                selectinload(MentorReview.student),
                selectinload(MentorReview.mentor).selectinload(Mentor.skills),
                selectinload(MentorReview.mentor).selectinload(Mentor.contacts),
            )
        )
        res = await self._session.execute(q)
        return res.scalars().all()
