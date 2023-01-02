import logging
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app import controllers
from app.database.depends import create_session
from app.schemas.applicant import (
    ApplicantResponseSchema,
    CreateApplicantRequestSchema
)

logger = logging.getLogger("__main__")

router = APIRouter(
    prefix="/applicants",
    tags=["applicants"]
)

GET_APPLICANT_STATUS_CODES = {
    200: {"description": "OK"},
    422: {"description": "Invalid input, params invalid."},
}

CREATE_APPLICANT_STATUS_CODES = {
    200: {"description": "OK"},
    201: {"description": "Applicant is Created"},
    204: {"description": "No Content"}
}


@router.post(
    "",
    response_model=ApplicantResponseSchema,
    responses=CREATE_APPLICANT_STATUS_CODES,    # type: ignore
    status_code=status.HTTP_200_OK
)
async def create_applicant(
        request: CreateApplicantRequestSchema,
        db: AsyncSession = Depends(create_session)
):
    logger.info("Create Applicant")
    return await controllers.applicant.create_applicant(db, request)
