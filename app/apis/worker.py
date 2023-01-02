import logging
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app import controllers
from app.database.depends import create_session
from app.schemas.worker import (
    WorkerResponseSchema,
    WorkerSchema,
    UpdateWorkerRequestSchema
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

UPDATE_WORKER_STATUS_CODES = {
    200: {"description": "OK"},
    202: {"description": "Accepted"},
    204: {"description": "No Content"}
}


@router.post(
    "",
    response_model=WorkerResponseSchema,
    responses=CREATE_WORKER_STATUS_CODES,    # type: ignore
    status_code=status.HTTP_201_CREATED
)
async def create_worker(
        worker: WorkerSchema,
        db: AsyncSession = Depends(create_session)
):
    logger.info("Create worker")
    return await controllers.worker.create_worker(db, worker)


@router.put(
    "/{worker_id}",
    response_model=WorkerResponseSchema,
    responses=UPDATE_WORKER_STATUS_CODES,    # type: ignore
    status_code=status.HTTP_200_OK
)
async def update_worker(
        worker_id: str,
        request: UpdateWorkerRequestSchema,
        db: AsyncSession = Depends(create_session)
):
    logger.info("Update worker")
    return await controllers.worker.update_worker(db, worker_id, request)
