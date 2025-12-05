from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.workers.tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

# Schedule
celery_app.conf.beat_schedule = {
    "fetch-energy-data-every-2-mins": {
        "task": "app.workers.tasks.fetch_and_process_data",
        "schedule": 120.0,  # 2 minutes
    },
}
