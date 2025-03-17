from celery import Celery

celery = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery.task
def heavy_ai_computation():
    """Run AI workloads in the background"""
    import time
    time.sleep(5)  # Simulate heavy AI processing
    return "AI Task Completed 🚀"

