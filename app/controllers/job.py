import logging
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.exceptions.configure_exceptions import ItemDoesNotExistErrorException
from app.schemas.job import (
    JobSchema,
    JobResponseSchema,
    GetJobsResponseSchema,
    SearchOptionsSchema
)
from app.database.models import Jobs, Workers, Applicants
from sqlalchemy import select
from app.utils.common import calculate_matching_score


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


async def get_job_recommendations(
        db: AsyncSession,
        worker_id: str,
        k: int = 10
):
    """Get Job Recommendations

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


async def get_jobs(
        db: AsyncSession,
        worker_id: str,
        search_options: SearchOptionsSchema
):
    """
    Get Job List

     Args:
        db (AsyncSession): database session
        worker_id (str): id of worker
        search_options (SearchOptionsSchema): search options payload

    Returns:
        GetJobsResponseSchema: return job information
    """
    return_jobs = []

    worker_stmt = select(Workers).filter(Workers.id == worker_id)
    worker_result = await db.execute(worker_stmt)
    worker = worker_result.scalar()
    if not worker:
        raise ItemDoesNotExistErrorException(item="Worker", item_id=worker_id)

    applied_jobs_stmt = select(Applicants.job_id).filter(Workers.id == worker_id)
    applied_jobs_result = await db.execute(applied_jobs_stmt)
    applied_jobs = applied_jobs_result.scalars().all()

    jobs_stmt = select(Jobs)
    if applied_jobs:
        jobs_stmt = jobs_stmt.filter(
            ~Jobs.id.in_(applied_jobs)
        )

    if search_options.discipline:
        jobs_stmt = jobs_stmt.filter(
            Jobs.discipline == search_options.discipline
        )

    if search_options.specialties:
        jobs_stmt = jobs_stmt.filter(
            Jobs.specialty.in_(search_options.specialties)
        )

    if search_options.state:
        jobs_stmt = jobs_stmt.filter(
            Jobs.state == search_options.state
        )

    if search_options.wage_min:
        jobs_stmt = jobs_stmt.filter(
            Jobs.pay_amount == search_options.wage_min
        )

    jobs_result = await db.execute(jobs_stmt)
    jobs = jobs_result.scalars().all()

    for job in jobs:
        return_jobs.append(
            {
                "job_id": job.id,
                "matching_score": calculate_matching_score(worker, job)
            }
        )

    return_jobs.sort(key=lambda x: x['matching_score'], reverse=True)

    return {
        "data": return_jobs
    }
