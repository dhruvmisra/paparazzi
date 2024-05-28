from typing import Annotated, List

from fastapi import APIRouter, File, Header

from config import AWS_REGION, SCREENSHOTS_S3_BUCKET_ENDPOINT, SCREENSHOTS_S3_BUCKET_NAME
from exceptions import (
    ApplicationException,
    InternalServerException,
    NotFoundException,
    RecordNotFoundException,
)
from log import log
from repositories import TestStepRepository
from schemas import (
    CreateTestStepRequest,
    CreateTestStepResponse,
    TestStepDBInput,
    TestStepResponse,
    UploadScreenshotResponse,
)
from util.id import get_user_test_id
from util.s3 import S3Helper

router = APIRouter()


@router.post("/{test_id}/steps", response_model=CreateTestStepResponse, status_code=201)
async def create_test_step(
    test_id: str,
    request: CreateTestStepRequest,
    user_id: str = Header(..., alias="x-user-id"),
):
    try:
        log.info(f"Creating test step for user_id: {user_id}, test_id: {test_id}")
        data = TestStepDBInput(user_test_id=get_user_test_id(user_id, test_id), **request.dict())
        item = TestStepRepository().create(data)
        return CreateTestStepResponse(id=item.id)
    except ApplicationException as e:
        raise e
    except Exception as e:
        InternalServerException(e)


@router.get("/{test_id}/steps", response_model=List[TestStepResponse])
async def list_test_steps(
    test_id: str,
    user_id: str = Header(..., alias="x-user-id"),
):
    try:
        log.info(f"Listing test steps for user_id: {user_id}, test_id: {test_id}")
        items = TestStepRepository().list(get_user_test_id(user_id, test_id))
        return [TestStepResponse(**item.dict()) for item in items]
    except ApplicationException as e:
        raise e
    except Exception as e:
        InternalServerException(e)


@router.get("/{test_id}/steps/{step_id}", response_model=TestStepResponse)
async def get_test_step(
    test_id: str,
    step_id: str,
    user_id: str = Header(..., alias="x-user-id"),
):
    try:
        log.info(
            f"Getting test step for user_id: {user_id}, test_id: {test_id}, step_id: {step_id}"
        )
        item = TestStepRepository().get(get_user_test_id(user_id, test_id), step_id)
        return TestStepResponse(**item.dict())
    except RecordNotFoundException as e:
        raise NotFoundException(e)
    except ApplicationException as e:
        raise e
    except Exception as e:
        InternalServerException(e)


@router.delete("/{test_id}/steps/{step_id}", status_code=204)
async def delete_test_step(
    test_id: str,
    step_id: str,
    user_id: str = Header(..., alias="x-user-id"),
):
    try:
        log.info(
            f"Deleting test step for user_id: {user_id}, test_id: {test_id}, step_id: {step_id}"
        )
        TestStepRepository().delete(get_user_test_id(user_id, test_id), step_id)
    except RecordNotFoundException as e:
        raise NotFoundException(e)
    except ApplicationException as e:
        raise e
    except Exception as e:
        InternalServerException(e)


@router.post(
    "/{test_id}/steps/{step_id}/screenshots",
    response_model=UploadScreenshotResponse,
    status_code=201,
)
async def upload_test_step_screenshot(
    test_id: str,
    step_id: str,
    file: Annotated[bytes, File(..., media_type="image/png")],
    user_id: str = Header(..., alias="x-user-id"),
):
    try:
        log.info(
            f"Uploading test step screenshot for user_id: {user_id}, test_id: {test_id}, step_id: {step_id}"
        )
        s3 = S3Helper(
            endpoint_url=SCREENSHOTS_S3_BUCKET_ENDPOINT, region=AWS_REGION, bucket_name=SCREENSHOTS_S3_BUCKET_NAME
        )
        response = s3.upload_file(
            file_path=f"{user_id}/{test_id}", file_name=f"{step_id}.png", body=file
        )
        log.info(f"Uploaded screenshot to S3: {response}")
        url = f"{SCREENSHOTS_S3_BUCKET_ENDPOINT}/{SCREENSHOTS_S3_BUCKET_NAME}/{user_id}/{test_id}/{step_id}.png"
        return UploadScreenshotResponse(url=url)
    except ApplicationException as e:
        raise e
    except Exception as e:
        InternalServerException(e)
