from fastapi import APIRouter

router = APIRouter()


@router.get("/health_check/liveness")
async def check_liveness():
    return {
        "probe": "liveness",
        "status": "ok"
    }
