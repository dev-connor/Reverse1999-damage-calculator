from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates

from reverse1999_damage_calculator.web.api.main.model import DEF

router = APIRouter()
templates = Jinja2Templates(directory="reverse1999_damage_calculator/static/")

@router.get("/")
def main(request: Request):

    return templates.TemplateResponse(
        "main.html",
        {
            "request": request,
            'data': DEF(bonus=0, spell=0, portray=0, buff=0),
        },
    )

@router.post("/")
def def_calculator(request: Request, req: DEF = Depends()):
    print(req)

    atk = req.atk
    spell = req.spell
    bonus = req.bonus
    norm_dmg = req.norm_dmg # 일반기술 데미지
    pen_dmg = req.pen_dmg # 방어무시기술 데미지
    buff = req.buff

    norm_pow = 180 # 일반기술 위력
    pen_pow = 120 # 방어무시기술 위력
    def_redn = 0 # 방어감소
    def_pen = 30 # 방어무시율

    if req.weakness:
        norm_pow = 200
        def_redn = 20
        if req.portray >= 1:
            norm_pow = 220
    if req.portray == 2:
        def_pen = 40

    # (공격력*(방무기술 데미지*일반기술 위력-일반기술 데미지*방무기술 위력))/(방무기술 데미지*일반기술 위력*(1-방어감소/100)-일반기술 데미지*방무기술 위력*(1-방어무시율/100)*(1-방어감소/100))
    defence = (atk*(pen_dmg*norm_pow-norm_dmg*pen_pow))/(pen_dmg*norm_pow*(1-def_redn/100)-norm_dmg*pen_pow*(1-def_pen/100)*(1-def_redn/100))

    # ((1-일반기술 데미지/((공격력-방어력*(1-방어감소/100))*(일반기술위력/100)*(1+마법위력/100))+피해보너스/100-피해감면/100)*100)
    dmg_taken = ((1-norm_dmg/((atk-defence*(1-def_redn/100))*(norm_pow/100)*(1+spell/100))+bonus/100-buff/100)*100)

    return templates.TemplateResponse(
        "main.html",
        {
            "request": request,
            "def": round(defence),
            "dmg_taken": round(dmg_taken),
            'data': req,
        },
    )
