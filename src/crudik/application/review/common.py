from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from crudik.models.mentor import MentorReview


class ReviewGateway(Protocol):
    @abstractmethod
    async def get_review(self, review_id: UUID) -> MentorReview | None: ...
