from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from crudik.application.data_model.mentor import MentorData
from crudik.models.mentoring_request import MentoringRequestType


class MentoringRequestData(BaseModel):
    id: UUID = Field(description="Mentorign request id")
    type: MentoringRequestType = Field(description="Mentorign type status")
    created_at: datetime = Field(description="Mentoring request create at")
    mentor: MentorData = Field(description="Mentorign request mentor data")
