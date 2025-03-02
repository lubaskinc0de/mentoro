from typing import Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from crudik.application.data_model.review import ReviewData
from crudik.application.review.add_review import AddReview, ReviewCreateData
from crudik.application.review.delete_review import DeleteReview

router = APIRouter(
    route_class=DishkaRoute,
    tags=["Reviews"],
    prefix="/review",
)

security = HTTPBearer(auto_error=False)


@router.post("/")
async def create_review(
    interactor: FromDishka[AddReview],
    data: ReviewCreateData,
    _token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> ReviewData:
    return await interactor.execute(data)


@router.delete("/{review_id}")
async def delete_review(
    interactor: FromDishka[DeleteReview],
    review_id: UUID,
    _token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> None:
    return await interactor.execute(review_id)
