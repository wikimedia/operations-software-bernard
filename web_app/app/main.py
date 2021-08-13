import uvicorn
from fastapi import FastAPI
from app.routes import apex
from fastapi.staticfiles import StaticFiles


def create_app() -> FastAPI:
    app = FastAPI(title="DBBackupsDashboard Bernard WebApp")
    app.include_router(apex.router)
    app.mount("/static", StaticFiles(directory="../static"), name="static")
    return app


APP = create_app()

if __name__ == "__main__":
    uvicorn.run(APP, host='0.0.0.0', port=8181)
