from celeryworker import celery_app
from log import log
from repositories import TestRepository, TestRunRepository, TestStepRepository


@celery_app.task(name="run_test")
def run_test(user_test_id: str, run_id: str):
    log.info(f"Running test for user_test_id: {user_test_id}, run_id: {run_id}")
    user_id = user_test_id.split("_")[0]
    test_id = user_test_id.split("_")[1]
    test_run = TestRunRepository().get(user_test_id, run_id)
    log.info(f"Test Run: {test_run}")
    test = TestRepository().get(user_id, test_id)
    log.info(f"Test: {test}")
    test_steps = TestStepRepository().list(user_test_id)
    log.info(f"Test Steps: {test_steps}")


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    log.info(f"Registering periodic tasks on {sender}")
    # add periodic tasks here
    log.info(f"Registered periodic tasks on {sender}")
