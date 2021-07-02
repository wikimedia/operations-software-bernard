""" Main module"""
import uvicorn
from fastapi import FastAPI
from app.routes.api.v1 import get_backups_data
from app.routes.health_check import liveness, readiness
from app.db import DatabaseConnection


APP_PORT: int = 8282


def create_app() -> FastAPI:
    app = FastAPI(title="DBBackupsDashboard Bernard API_DB")
    app.include_router(get_backups_data.router)
    app.include_router(liveness.ROUTER)
    app.include_router(readiness.router)
    return app


APP = create_app()


@APP.on_event("startup")
async def startup():
    await DatabaseConnection.instance().database.connect()


@APP.on_event("shutdown")
async def shutdown():
    await DatabaseConnection.instance().database.disconnect()


if __name__ == "__main__":
    uvicorn.run(APP, host='0.0.0.0', port=APP_PORT)
