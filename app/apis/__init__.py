from fastapi import FastAPI
from app.config import config
from app.apis import job, worker, applicant

def configure_routes(app: FastAPI):
    app.include_router(router=job.router, prefix=config.OPENAPI_PREFIX)
    app.include_router(router=worker.router, prefix=config.OPENAPI_PREFIX)
    app.include_router(router=applicant.router, prefix=config.OPENAPI_PREFIX)
