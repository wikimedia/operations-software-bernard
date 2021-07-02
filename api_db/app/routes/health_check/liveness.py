from fastapi import APIRouter

ROUTER = APIRouter()


@ROUTER.get("/health_check/liveness")
async def check_liveness():
    return {
        "probe": "liveness",
        "status": "ok"
    }
