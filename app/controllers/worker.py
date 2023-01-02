import logging
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.exceptions.configure_exceptions import ItemDoesNotExistErrorException
from app.schemas.worker import (
    WorkerSchema,
    WorkerResponseSchema,
    UpdateWorkerRequestSchema
)
from app.database.models import Workers


logger = logging.getLogger("__main__")


async def create_worker(
        db: AsyncSession,
        worker: WorkerSchema,
):
    """
    Create Worker
    
    Args:
        db (AsyncSession): database session
        worker (WorkerSchema): input worker data

    Returns:
        WorkerResponseSchema: return worker information
    """

    _worker = Workers(
        id=str(uuid.uuid4()),
        discipline=worker.discipline,
        specialties=list(set(specialty for specialty in worker.specialties)),
        preferred_working_states=list(set(state for state in worker.preferred_working_states)),
        avg_weekly_pay_amount=worker.avg_weekly_pay_amount,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    db.add(_worker)
    await db.commit()
    await db.refresh(_worker)

    return _worker


async def update_worker(
        db: AsyncSession,
        worker_id: str,
        request: UpdateWorkerRequestSchema
):
    """
    Update Worker

     Args:
        db (AsyncSession): database session
        worker_id (str): worker id
        request (UpdateWorkerRequestSchema): update worker data

    Returns:
        WorkerResponseSchema: return worker information
    """
    worker_stmt = select(Workers).filter(Workers.id == worker_id)
    worker_result = await db.execute(worker_stmt)
    worker = worker_result.scalar()

    if not worker:
        raise ItemDoesNotExistErrorException(item="Worker", item_id=worker_id)

    updated_worker = request.dict(exclude_unset=True)

    if "updated_at" not in updated_worker:
        updated_worker["updated_at"] = datetime.now()

    for key, value in updated_worker.items():
        setattr(worker, key, value)

    db.add(worker)
    await db.commit()
    await db.refresh(worker)

    return worker
