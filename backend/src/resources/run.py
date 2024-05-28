from typing import List

from fastapi import APIRouter, Header

from constants import TestResultStatus, TestRunState
from exceptions import (
    ApplicationException,
    InternalServerException,
    NotFoundException,
    RecordNotFoundException,
)
from jobs import run_test
from log import log
from repositories import TestRunRepository
from schemas import QueueTestRunResponse, TestRunDBInput, TestRunResponse, TestRunResult
from util.id import get_user_test_id

router = APIRouter()


@router.post("/{test_id}/run", response_model=QueueTestRunResponse, status_code=201)
async def queue_test_run(
    test_id: str,
    user_id: str = Header(..., alias="x-user-id"),
):
    try:
        log.info(f"Queuing test run for user_id: {user_id}, test_id: {test_id}")
        user_test_id = get_user_test_id(user_id, test_id)
        data = TestRunDBInput(
            user_test_id=user_test_id,
            state=TestRunState.QUEUED,
            result=TestRunResult(status=TestResultStatus.PENDING, steps=[]),
        )
        item = TestRunRepository().create(data)
        run_test.apply_async(
            (user_test_id, item.id),
        )
        return QueueTestRunResponse(id=item.id, message="Test run queued")
    except ApplicationException as e:
        raise e
    except Exception as e:
        log.error(f"Error queuing test run: {e}")
        InternalServerException(e)


@router.get("/{test_id}/runs", response_model=List[TestRunResponse])
async def list_test_runs(
    test_id: str,
    user_id: str = Header(..., alias="x-user-id"),
):
    try:
        log.info(f"Listing test runs for user_id: {user_id}, test_id: {test_id}")
        items = TestRunRepository().list(get_user_test_id(user_id, test_id))
        return [TestRunResponse(**item.dict()) for item in items]
    except ApplicationException as e:
        raise e
    except Exception as e:
        InternalServerException(e)


@router.get("/{test_id}/runs/{run_id}", response_model=TestRunResponse)
async def get_test_run(
    test_id: str,
    run_id: str,
    user_id: str = Header(..., alias="x-user-id"),
):
    try:
        log.info(f"Getting test run for user_id: {user_id}, test_id: {test_id}, run_id: {run_id}")
        item = TestRunRepository().get(get_user_test_id(user_id, test_id), run_id)
        return TestRunResponse(**item.dict())
    except RecordNotFoundException as e:
        raise NotFoundException(e)
    except ApplicationException as e:
        raise e
    except Exception as e:
        InternalServerException(e)
