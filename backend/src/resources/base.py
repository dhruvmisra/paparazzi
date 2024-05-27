from fastapi import APIRouter

from config import ENVIRONMENT, VERSION
from routes import create_router

router: APIRouter = create_router()


@router.get("/")
async def base_route():
    return {
        "server": "zeus",
        "environment": ENVIRONMENT,
        "version": VERSION,
    }
