from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

import config
from exceptions import add_exception_handlers
from log import log
from resources import health, run, step, test
from util.security_headers import add_security_headers

log.warning("██████╗  █████╗ ██████╗  █████╗ ██████╗  █████╗ ███████╗███████╗██╗")
log.warning("██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗╚══███╔╝╚══███╔╝██║")
log.warning("██████╔╝███████║██████╔╝███████║██████╔╝███████║  ███╔╝   ███╔╝ ██║")
log.warning("██╔═══╝ ██╔══██║██╔═══╝ ██╔══██║██╔══██╗██╔══██║ ███╔╝   ███╔╝  ██║")
log.warning("██║     ██║  ██║██║     ██║  ██║██║  ██║██║  ██║███████╗███████╗██║")
log.warning("╚═╝     ╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝")

app = FastAPI(
    title="paparazzi",
    version="v1",
    docs_url="/docs" if config.DEBUG else None,
    redoc_url="/redoc" if config.DEBUG else None,
    openapi_url="/openapi.json" if config.DEBUG else None,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["OPTIONS", "GET", "POST", "PATCH", "PUT", "DELETE"],
    allow_headers=["*"],
)
app.add_middleware(CorrelationIdMiddleware)
add_security_headers(app)
add_exception_handlers(app)

api_router = APIRouter(prefix="/v1")
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(test.router, prefix="/tests", tags=["test"])
api_router.include_router(step.router, prefix="/tests", tags=["test-step"])
api_router.include_router(run.router, prefix="/tests", tags=["test-run"])
app.include_router(api_router)
