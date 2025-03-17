from fastapi import FastAPI
from app.api.routes import ai, users, health

app = FastAPI(title="AI System", version="1.0")

# Register API routes
app.include_router(health.router,prefix="/health",tags=["Health"])
app.include_router(users.router,prefix="/users",tags=["Users"])
app.include_router(ai.router,prefix="/ai",tags=["AI"])

@app.get("/")
async def root():
    return {"message":"AI system is Running"}



# from fastapi import FastAPI, BackgroundTasks
# import pandas as pd
# import asyncio
# from celery import Celery

# app = FastAPI()

# # Celery Configuration
# celery = Celery(
#     "tasks",
#     broker="redis://localhost:6379/0",
#     backend="redis://localhost:6379/0"
# )

# @app.get("/")
# async def root():
#     return {"message": "FastAPI AI System Running 🚀"}

# @app.post("/process-data/")
# async def process_data(background_tasks: BackgroundTasks):
#     """Handles AI data processing asynchronously."""
#     background_tasks.add_task(run_ai_task)
#     return {"message": "Processing started in the background"}

# @app.get("/basic")
# async def basic_func():
#     return {"message": "ith charithram"}

# @celery.task
# def run_ai_task():
#     """Background AI processing task"""
#     df = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})
#     df["sum"] = df["col1"] + df["col2"]
#     print("Processed Data:\n", df)

