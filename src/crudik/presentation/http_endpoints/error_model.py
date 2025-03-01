from pydantic import BaseModel, Field


class ErrorModel(BaseModel):
    code: str = Field(description="Unique error code")
