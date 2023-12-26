import uvicorn

from reverse1999_damage_calculator.settings import settings


def main() -> None:
    """Entrypoint of the application."""
    uvicorn.run(
        "reverse1999_damage_calculator.web.application:get_app",
        workers=settings.workers_count,
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.value.lower(),
        factory=True,
    )


if __name__ == "__main__":
    main()
