import logging
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.exceptions.configure_exceptions import ItemDoesNotExistErrorException
from app.schemas.job import (
    JobSchema,
    JobResponseSchema,
    GetJobsResponseSchema,
)
from app.database.models import Jobs, Workers
from sqlalchemy import select
from app.utils.common import calculate_matching_score


logger = logging.getLogger("__main__")

async def create_job(
        db: AsyncSession,
        job: JobSchema,
):
    """
    Create Job

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


async def get_job_recommendations(
        db: AsyncSession,
        worker_id: str,
        k: int = 10
):
    """
    Get Job Recommendations

     Args:
        db (AsyncSession): database session
        k (int): top k result
        worker_id (str): worker id

    Returns:
        GetJobsResponseSchema: return job information
    """

    worker_stmt = select(Workers).filter(Workers.id == worker_id)
    worker_result = await db.execute(worker_stmt)
    worker = worker_result.scalar()
    if not worker:
        raise ItemDoesNotExistErrorException(item="Worker", item_id=worker_id)

    job_stmt = select(Jobs)
    job_result = await db.execute(job_stmt)
    jobs = job_result.scalars().all()
    job_recommendations = []

    for job in jobs:
        job_recommendations.append(
            {
                "job_id": job.id,
                "matching_score": calculate_matching_score(worker, job)
            }
        )

    job_recommendations.sort(key=lambda x: x['matching_score'], reverse=True)
    job_recommendations = job_recommendations[:k]

    return {
        "data": job_recommendations
    }
