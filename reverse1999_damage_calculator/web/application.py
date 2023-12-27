from importlib import metadata

from fastapi import FastAPI
from fastapi.responses import UJSONResponse

from reverse1999_damage_calculator.web.api.router import api_router, view_router
from reverse1999_damage_calculator.web.lifetime import (
    register_shutdown_event,
    register_startup_event,
)


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    app = FastAPI(
        title="reverse1999_damage_calculator",
        version=metadata.version("reverse1999_damage_calculator"),
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")
    app.include_router(router=view_router, prefix="")

    return app
