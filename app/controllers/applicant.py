import logging
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.configure_exceptions import ItemDoesNotExistErrorException
from app.schemas.applicant import (
    CreateApplicantRequestSchema,
    ApplicantResponseSchema
)
from app.database.models import Applicants, Workers, Jobs
from sqlalchemy import select


logger = logging.getLogger("__main__")


async def create_applicant(
        db: AsyncSession,
        request: CreateApplicantRequestSchema,
):
    """
    Create Applicant

    Args:
        db (AsyncSession): database session
        request (CreateApplicantRequestSchema): input data

    Returns:
        ApplicantResponseSchema: return applicant information
    """
    worker_stmt = select(Workers).filter(Workers.id == request.worker_id)
    worker_result = await db.execute(worker_stmt)
    worker = worker_result.scalar()

    if not worker:
        raise ItemDoesNotExistErrorException(item="Worker", item_id=request.worker_id)

    job_stmt = select(Jobs).where(Jobs.id == request.job_id)
    job_result = await db.execute(job_stmt)
    job = job_result.scalar()

    if not job:
        raise ItemDoesNotExistErrorException(item="Job", item_id=request.job_id)

    applicant_stmt = select(Applicants).filter(
        Applicants.worker_id == request.worker_id,
        Applicants.job_id == request.job_id
    )
    applicant_result = await db.execute(applicant_stmt)
    applicant = applicant_result.scalar()

    if applicant:
        raise Exception(f"This applicant between worker {request.worker_id} "
                        f"and job {request.job_id} is existed")

    _applicant = Applicants(
        job_id=request.job_id,
        worker_id=request.worker_id
    )

    db.add(_applicant)
    await db.commit()
    await db.refresh(_applicant)

    applicant = {
        "id": _applicant.id,
        "job": job,
        "worker": worker
    }

    return applicant
