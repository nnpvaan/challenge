import logging
from typing import Union, List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app import controllers
from app.database.depends import create_session
from app.schemas.job import (
    JobResponseSchema,
    JobSchema,
)

logger = logging.getLogger("__main__")

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"]
)

CREATE_JOB_STATUS_CODES = {
    200: {"description": "OK"},
    201: {"description": "Job is Created"},
    204: {"description": "No Content"}
}


@router.post(
    "",
    response_model=JobResponseSchema,
    responses=CREATE_JOB_STATUS_CODES,    # type: ignore
    status_code=status.HTTP_200_OK
)
async def create_job(
        job: JobSchema,
        db: AsyncSession = Depends(create_session)
):
    logger.info("Create Job")
    return await controllers.job.create_job(db, job)
