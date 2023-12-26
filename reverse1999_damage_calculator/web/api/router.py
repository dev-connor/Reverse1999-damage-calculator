from fastapi.routing import APIRouter

from reverse1999_damage_calculator.web import static
from reverse1999_damage_calculator.web.api import echo, monitoring

api_router = APIRouter()
static_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])

static_router.include_router(static.router)
