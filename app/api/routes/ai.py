from fastapi import APIRouter,BackgroundTasks

router = APIRouter()


@router.get("/ai-process")
async def AI_PROCESS():
    print("AI prcocees done")
    return {message:"done"}