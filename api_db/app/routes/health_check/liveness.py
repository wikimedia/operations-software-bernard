from fastapi import APIRouter

router = APIRouter()


@router.get("/health_check/readiness")
async def check_readiness():
    # TODO readiness means that our app is responding to requests and can connect to sql db
    # Add functionality to perform db connection, and then return error accordingly
    return {
        "probe": "readiness",
        "status": "ok"
    }
