from celery import Celery
from .settings import settings

celery_app = Celery(
    "analyzer_tasks",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)


celery_app.autodiscover_tasks(["src.services.analyzer.app"])
