from pydantic import BaseModel
from pydantic.types import conlist
from app.database.models import Discipline, State, Specialty


class WorkerSchema(BaseModel):
    discipline: Discipline
    specialties: conlist(Specialty, min_items=1, max_items=2)
    preferred_working_states: conlist(State, min_items=1, max_items=2)
    avg_weekly_pay_amount: float

    class Config:
        use_enum_values = True

class WorkerResponseSchema(WorkerSchema):
    id: str

    class Config:
        orm_mode = True


class UpdateWorkerRequestSchema(BaseModel):
    avg_weekly_pay_amount: float
