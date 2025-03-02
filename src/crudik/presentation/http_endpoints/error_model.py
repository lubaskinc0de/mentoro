from pydantic import BaseModel, Field


class ErrorModel(BaseModel):
    code: str = Field(description="Уникальный код ошибки")
