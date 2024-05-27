from celeryworker import celery_app
from log import log


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    log.info(f"Registering periodic tasks on {sender}")
    # add periodic tasks here
    log.info(f"Registered periodic tasks on {sender}")
