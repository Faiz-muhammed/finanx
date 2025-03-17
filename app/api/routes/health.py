from fastapi import APIRouter, BackgroundTasks
# from app.

router = APIRouter()

@router.get("/system-health")
async def SYSTEM_HEALTH():
    return{"message":"system health is OK"}