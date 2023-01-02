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
