from worker.app.celery_app import celery_app


@celery_app.task
def run_fixture_scan(scan_id: str):
    return {'status': 'completed', 'scan_id': scan_id}
