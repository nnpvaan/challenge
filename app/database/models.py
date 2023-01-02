import enum
import uuid
from datetime import datetime
from sqlalchemy import Column, ForeignKey, DateTime, Integer, Float, String, ARRAY, Enum
from sqlalchemy.orm import relationship
from app.database.config import BaseMixin, BaseModel


class Discipline(str, enum.Enum):
    RN = "RN"
    LPN_LVN = "LPN/LVN"
    PHYSICAL_THERAPIST = "PHYSICAL THERAPIST"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class Specialty(str, enum.Enum):
    ICU = "ICU"
    PCU = "PCU"
    DIALYSIS = "DIALYSIS"
    CVOR = "CVOR"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class State(str, enum.Enum):
    CA = "CA"
    TX = "TX"
    NY = "NY"
    MN = "MN"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class Workers(BaseMixin, BaseModel):
    id = Column(String, nullable=False, primary_key=True, index=True, default=str(uuid.uuid4()))
    discipline = Column(Enum(Discipline), nullable=False)
    specialties = Column(ARRAY(Enum(Specialty)),nullable=False)
    preferred_working_states = Column(ARRAY(Enum(State)), nullable=False)
    avg_weekly_pay_amount = Column(Float, nullable=False)
    created_at = Column(DateTime(), nullable=False, default=datetime.now)
    updated_at = Column(DateTime(), nullable=False, default=datetime.now)


class Jobs(BaseMixin, BaseModel):
    id = Column(String, nullable=False, primary_key=True, index=True, default=str(uuid.uuid4()))
    discipline = Column(Enum(Discipline), nullable=False)
    specialty = Column(Enum(Specialty), nullable=False)
    state = Column(Enum(State), nullable=False)
    pay_amount = Column(Float, nullable=False)
    created_at = Column(DateTime(), nullable=False, default=datetime.now)
    updated_at = Column(DateTime(), nullable=False, default=datetime.now)


class Applicants(BaseMixin, BaseModel):
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True, index=True)
    worker_id = Column(String, ForeignKey("workers.id"), nullable=False)
    worker = relationship(
        "Workers", backref="applicants_workers", cascade="all,delete"
    )
    job_id = Column(String, ForeignKey("jobs.id"), nullable=False)
    job = relationship(
        "Jobs", backref="applicants_jobs", cascade="all,delete"
    )
