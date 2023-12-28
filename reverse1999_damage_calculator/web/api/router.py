from fastapi.routing import APIRouter

from reverse1999_damage_calculator.web.api import echo, monitoring, main

api_router = APIRouter()
view_router = APIRouter()

api_router.include_router(monitoring.router)
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])

view_router.include_router(main.router)
