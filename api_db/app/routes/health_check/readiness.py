from fastapi import APIRouter, HTTPException
from app.controller import crud

router = APIRouter()


@router.get("/health_check/readiness")
async def check_readiness():
    # Readiness means that our app is responding to requests and
    # can connect to sql db and return some result
    res = await crud.readiness_check()
    if len(res) > 0:
        return {
            "probe": "readiness",
            "status": "ok"
        }
    raise HTTPException(status_code=500, detail="Readiness probe failed")
