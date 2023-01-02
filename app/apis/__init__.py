from fastapi import FastAPI
from app.config import config
from app.apis import job

def configure_routes(app: FastAPI):
    app.include_router(router=job.router, prefix=config.OPENAPI_PREFIX)
