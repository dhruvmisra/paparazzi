from typing import List

from fastapi import APIRouter, Header

from constants import TestState
from exceptions import (
    ApplicationException,
    BadRequestException,
    InternalServerException,
    NotFoundException,
    RecordNotFoundException,
)
from jobs import complete_test_recording
from log import log
from repositories import TestRepository
from schemas import (
    CreateTestRequest,
    TestDBInput,
    TestResponse,
    UpdateTestRequest,
)

router = APIRouter()


@router.post("", response_model=TestResponse, status_code=201)
async def create_test(
    request: CreateTestRequest,
    user_id: str = Header(..., alias="x-user-id"),
):
    try:
        log.info(f"Creating test for user_id: {user_id}")
        data = TestDBInput(user_id=user_id, state=TestState.RECORDING, **request.dict())
        item = TestRepository().create(data)
        return TestResponse(**item.dict())
    except ApplicationException as e:
        raise e
    except Exception as e:
        raise InternalServerException(e)


@router.get("", response_model=List[TestResponse])
async def list_tests(
    user_id: str = Header(..., alias="x-user-id"),
):
    try:
        log.info(f"Listing tests for user_id: {user_id}")
        items = TestRepository().list(user_id)
        return [TestResponse(**item.dict()) for item in items]
    except ApplicationException as e:
        raise e
    except Exception as e:
        raise InternalServerException(e)


@router.get("/{test_id}", response_model=TestResponse)
async def get_test(
    test_id: str,
    user_id: str = Header(..., alias="x-user-id"),
):
    try:
        log.info(f"Getting test for user_id: {user_id}, test_id: {test_id}")
        item = TestRepository().get(user_id, test_id)
        return TestResponse(**item.dict())
    except RecordNotFoundException as e:
        raise NotFoundException(e)
    except ApplicationException as e:
        raise e
    except Exception as e:
        raise InternalServerException(e)


@router.post("/{test_id}/complete", response_model=TestResponse)
async def queue_test_for_completion(
    test_id: str,
    user_id: str = Header(..., alias="x-user-id"),
):
    try:
        log.info(f"Queuing test for completion for user_id: {user_id}, test_id: {test_id}")
        item = TestRepository().get(user_id, test_id)
        # if item.state != TestState.RECORDING:
        #     raise BadRequestException(detail="Test is not in recording state")

        complete_test_recording.apply_async(
            (user_id, test_id),
        )
        item.state = TestState.QUEUED
        item = TestRepository().update(item, user_id, test_id)
        return TestResponse(**item.dict())
    except RecordNotFoundException as e:
        raise NotFoundException(e)
    except ApplicationException as e:
        raise e
    except Exception as e:
        raise InternalServerException(e)


@router.patch("/{test_id}", response_model=TestResponse)
async def update_test(
    test_id: str,
    request: UpdateTestRequest,
    user_id: str = Header(..., alias="x-user-id"),
):
    try:
        log.info(f"Updating test for user_id: {user_id}, test_id: {test_id}")
        item = TestRepository().update(request, user_id, test_id)
        return TestResponse(**item.dict())
    except RecordNotFoundException as e:
        raise NotFoundException(e)
    except ApplicationException as e:
        raise e
    except Exception as e:
        raise InternalServerException(e)


@router.delete("/{test_id}", status_code=204)
async def delete_test(
    test_id: str,
    user_id: str = Header(..., alias="x-user-id"),
):
    try:
        log.info(f"Deleting test for user_id: {user_id}, test_id: {test_id}")
        TestRepository().delete(user_id, test_id)
    except RecordNotFoundException as e:
        raise NotFoundException(e)
    except ApplicationException as e:
        raise e
    except Exception as e:
        raise InternalServerException(e)
