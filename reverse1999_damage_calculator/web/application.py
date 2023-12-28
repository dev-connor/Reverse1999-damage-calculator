from importlib import metadata

from fastapi import FastAPI, Request
from fastapi.responses import UJSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles

from reverse1999_damage_calculator.web.api.main.view import templates
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

    app.mount("/templates", StaticFiles(directory="reverse1999_damage_calculator/templates/"), name="templates")

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")
    app.include_router(router=view_router, prefix="")

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return templates.TemplateResponse("500/index.html", {"request": request,"detail": "Validation error"},status_code=500)

    return app
