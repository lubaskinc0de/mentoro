from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

router = APIRouter(
    tags=["Система"],
    route_class=DishkaRoute,
)


@router.get("/ping")
async def ping() -> str:
    return "pong"
