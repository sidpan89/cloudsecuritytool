from celery import Celery
import os

broker_url = os.getenv('REDIS_URL', 'redis://redis:6379/0')
backend_url = broker_url

celery_app = Celery('worker', broker=broker_url, backend=backend_url)
celery_app.autodiscover_tasks(['worker.app.tasks'])
