from typing import List, Optional
from pydantic import BaseModel
from app.database.models import Discipline, State, Specialty


class JobSchema(BaseModel):
    discipline: Discipline
    specialty: Specialty
    state: State
    pay_amount: float

    class Config:
        use_enum_values = True

class JobResponseSchema(JobSchema):
    id: str

    class Config:
        orm_mode = True


class GetJobsSchema(BaseModel):
    job_id: str
    matching_score: float


class GetJobsResponseSchema(BaseModel):
    data: List[GetJobsSchema]


class SearchOptionsSchema(BaseModel):
    discipline: Optional[Discipline]
    specialties: Optional[List[Specialty]]
    state: Optional[State]
    wage_min: Optional[float]

    class Config:
        use_enum_values = True
