from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates

from reverse1999_damage_calculator.web.api.main.model import DEF

router = APIRouter()
templates = Jinja2Templates(directory="reverse1999_damage_calculator/static/")

@router.get("/")
def health_check(request: Request):

    return templates.TemplateResponse(
        "main.html",
        {
            "request": request,
            "message": "hello",
            "def": 11,
            "dmg_taken": 22,
        },
    )
@router.post("/")
def health_check(request: Request, req: DEF = Depends()):

    print(req.atk)
    print(req.dmg)
    print(req.spell)

    return templates.TemplateResponse(
        "main.html",
        {
            "request": request,
            "message": "hello",
            "def": req.atk + req.dmg + req.spell,
            "dmg_taken": 22,
            'req': req,
        },
    )
