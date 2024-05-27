from fastapi import APIRouter

from log import log
from schemas import HealthResponse

router = APIRouter()


@router.get("", response_model=HealthResponse)
async def health():
    log.debug("Health check")
    return HealthResponse()
