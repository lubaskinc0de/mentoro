from typing import Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, Path
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from crudik.application.data_model.review import ReviewData, ReviewFullData
from crudik.application.review.add_review import AddReview, ReviewCreateData
from crudik.application.review.delete_review import DeleteReview
from crudik.application.review.read_profile_reviews import ReadMentorProfileReviews
from crudik.application.review.read_reviews import ReadMentorReviewsByStudent
from crudik.presentation.http_endpoints.error_model import ErrorModel

router = APIRouter(
    route_class=DishkaRoute,
    tags=["Отзывы"],
    prefix="/review",
)

security = HTTPBearer(auto_error=False)


@router.post(
    "/",
    description="Добавление отзыва ментеру",
    responses={
        200: {
            "description": "Успешно добавлен отзыв",
            "model": ReviewData,
        },
        401: {
            "description": "Студент не авторизован",
            "model": ErrorModel,
        },
        403: {
            "description": "Отзыв не может быть создан (не одобрена заявка к ментору)",
            "model": ErrorModel,
        },
    },
)
async def add_review(
    interactor: FromDishka[AddReview],
    data: ReviewCreateData,
    _token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> ReviewData:
    return await interactor.execute(data)


@router.delete(
    "/{review_id}",
    description="Удаление отзыва",
    responses={
        200: {
            "description": "Успешное удаление отзыва",
        },
        401: {
            "description": "Студент не авторизован",
            "model": ErrorModel,
        },
        403: {
            "model": ErrorModel,
            "description": "Отзыв создан другим пользователем",
        },
        404: {
            "model": ErrorModel,
            "description": "Отзыв не существует",
        },
    },
)
async def delete_review(
    interactor: FromDishka[DeleteReview],
    review_id: Annotated[UUID, Path(description="Идентификатор отзыв")],
    _token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> None:
    return await interactor.execute(review_id)


@router.get(
    "/{mentor_id}",
    description="Получение всех отзывов ментора",
    responses={
        200: {
            "model": list[ReviewFullData],
            "description": "Успешное получение отзывов ментора",
        },
        401: {
            "model": ErrorModel,
            "description": "Студент не авторизован",
        },
    },
)
async def mentor_reviews(
    interactor: FromDishka[ReadMentorReviewsByStudent],
    mentor_id: Annotated[UUID, Path(description="Идентификатор ментора")],
    _token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> list[ReviewFullData]:
    return await interactor.execute(mentor_id)


@router.get(
    "/",
    description="Получение всех отзывов авторизованного ментора",
    responses={
        200: {
            "model": list[ReviewFullData],
            "description": "Успешное получение отзывов ментора",
        },
        401: {
            "model": ErrorModel,
            "description": "Ментор не авторизован",
        },
    },
)
async def mentor_profile_reviews(
    interactor: FromDishka[ReadMentorProfileReviews],
    _token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> list[ReviewFullData]:
    return await interactor.execute()
