from pydantic import BaseModel
from app.database.models import Discipline, State, Specialty
from pydantic.types import conlist


class JobApplicantSchema(BaseModel):
    id: str
    discipline: Discipline
    specialty: Specialty
    state: State
    pay_amount: float

    class Config:
        use_enum_values = True
        orm_mode = True


class WorkerApplicantSchema(BaseModel):
    id: str
    discipline: Discipline
    specialties: conlist(Specialty, min_items=1, max_items=2)
    preferred_working_states: conlist(State, min_items=1, max_items=2)
    avg_weekly_pay_amount: float

    class Config:
        use_enum_values = True
        orm_mode = True


class CreateApplicantRequestSchema(BaseModel):
    job_id: str
    worker_id: str


class ApplicantResponseSchema(BaseModel):
    id: int
    job: JobApplicantSchema
    worker: WorkerApplicantSchema
