from fastapi import FastAPI
from app.config.app_config import get_settings, Settings
from typing import Optional
from app.routes.api.v1 import get_backups_data
from app.routes.health_check import liveness, readiness
import uvicorn

APP_PORT: int = 8282

app = FastAPI()
app.include_router(get_backups_data.router)
app.include_router(liveness.router)
app.include_router(readiness.router)


@app.get("/show_environment")
async def show_environment():
    settings: Optional[Settings] = get_settings()
    if settings.environment_endpoint_active is True:
        return {
            "ping": "pong!",
            "environment": settings.environment,
            "testing": settings.testing
        }
    else:
        return {"ping": "Endpoint inactive"}


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=APP_PORT)
