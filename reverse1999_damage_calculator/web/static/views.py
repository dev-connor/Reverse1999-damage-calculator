from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="reverse1999_damage_calculator/templates/")


@router.get("/")
def health_check(request: Request):
    return templates.TemplateResponse(
        "main.html",
        {
            "request": request,
            "message": "hello",
        },
    )
