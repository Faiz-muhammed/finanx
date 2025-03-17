from fastapi import APIRouter,BackgroundTasks

router = APIRouter()

@router.get("/user")
async def GET_USER():
    return {message:"this is a user"}