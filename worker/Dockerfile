FROM python:3.11-slim
WORKDIR /worker
COPY worker/requirements.txt /worker/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY worker /worker
ENV PYTHONPATH=/worker
CMD ["celery", "-A", "worker.app.celery_app.celery_app", "worker", "--loglevel=info"]
