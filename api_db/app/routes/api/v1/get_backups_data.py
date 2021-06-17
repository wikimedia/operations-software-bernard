from fastapi import APIRouter

router = APIRouter()


# TODO database logic

@router.get("/api/v1/get_recent_backups_data")
async def get_recent_backups_data():
    return {"status": "todo!"}


@router.get("/api/v1/get_backups_data_by_section")
async def get_backups_data_by_section():
    return {"status": "todo!"}


@router.get("/api/v1/get_backups_data_by_time")
async def get_backups_data_by_time():
    return {"status": "todo!"}
