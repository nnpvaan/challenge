import logging
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app import controllers
from app.database.depends import create_session
from app.schemas.worker import (
    WorkerResponseSchema,
    WorkerSchema,
)

logger = logging.getLogger("__main__")

router = APIRouter(
    prefix="/workers",
    tags=["workers"]
)

CREATE_WORKER_STATUS_CODES = {
    200: {"description": "OK"},
    201: {"description": "Worker is Created"},
    204: {"description": "No Content"}
}


@router.post(
    "",
    response_model=WorkerResponseSchema,
    responses=CREATE_WORKER_STATUS_CODES,    # type: ignore
    status_code=status.HTTP_200_OK
)
async def create_worker(
        worker: WorkerSchema,
        db: AsyncSession = Depends(create_session)
):
    logger.info("Create worker")
    return await controllers.worker.create_worker(db, worker)
