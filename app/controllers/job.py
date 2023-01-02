import logging
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.job import (
    JobSchema,
    JobResponseSchema
)
from app.database.models import Jobs


logger = logging.getLogger("__main__")

async def create_job(
        db: AsyncSession,
        job: JobSchema,
):
    """Create Job
     Args:
        db (AsyncSession): database session
        job (JobSchema): input job data
    Returns:
        JobResponseSchema: return job information
    """

    _job = Jobs(
        id=str(uuid.uuid4()),
        discipline=job.discipline,
        specialty=job.specialty,
        state=job.state,
        pay_amount=job.pay_amount,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    db.add(_job)
    await db.commit()
    await db.refresh(_job)

    return _job
