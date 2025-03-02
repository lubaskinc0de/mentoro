from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from crudik.application.data_model.mentor import MentorData
from crudik.models.mentoring_request import MentoringRequestType


class MentoringRequestData(BaseModel):
    id: UUID = Field(description="Идентификатор заявки на ментерство")
    type: MentoringRequestType = Field(description="Тип заявки на ментерство")
    created_at: datetime = Field(description="Дата создания заявки на ментерство")
    mentor: MentorData = Field(description="Данные ментора")
