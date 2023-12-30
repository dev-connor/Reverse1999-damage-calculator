from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError

from reverse1999_damage_calculator.web.api.main.model import DEF,DMG

router = APIRouter()
templates = Jinja2Templates(directory="reverse1999_damage_calculator/templates/")

@router.get("/")
def main(request: Request):

    return templates.TemplateResponse(
        "def_calculator.html",
        {
            "request": request,
            "tag": 'def',
            'data': DEF(stat_bonus=0, psy_bonus=0, spell=0, portray=0, buff=0, weakness=False, afflatus=False),
        },
    )
@router.get("/dmg-calculator")
def dmg_main(request: Request):

    return templates.TemplateResponse(
        "dmg_calculator.html",
        {
            "request": request,
            "tag": 'dmg',
            'data': DMG(afflatus=False, stat_bonus=0, inherit_atk=0, inherit_bonus=0, psy_bonus=0, spell=0, def_redn=0, buff=0, debuff=0),
        },
    )

@router.post("/dmg-calculator")
def dmg_calculator(request: Request, req: DMG = Depends()):
    print(req)

    atk = req.atk
    power = req.power
    stat_bonus = req.stat_bonus
    inherit_atk = req.inherit_atk
    inherit_bonus = req.inherit_bonus
    spell = req.spell
    psy_bonus = req.psy_bonus

    # 적군
    defence = req.defence
    dmg_taken = req.dmg_taken

    # 환경
    def_redn = req.def_redn
    buff = req.buff
    debuff = req.debuff

    afflatus = 1
    if req.afflatus:
        afflatus = 1.3

    # (공격*(1+특성공격/100)-적군방어*(1-방어감소/100))*기술위력/100*(1+(특성 피해보너스+아군 스탯 피해보너스+적군 피해보너스-적군 피해감면-적군 스탯 피해감면)/100)*상성*(1+마법위력/100)
    dmg = (atk*(1+inherit_atk/100)-defence*(1-def_redn/100))*power/100*(1+(inherit_bonus+stat_bonus+psy_bonus+debuff-buff-dmg_taken)/100)*afflatus*(1+spell/100)
    print(dmg)

    return templates.TemplateResponse(
        "dmg_calculator.html",
        {
            "request": request,
            "data": req,
            "tag": 'dmg',
            "dmg": round(dmg),
        },
    )

@router.get("/about")
def about(request: Request):

    return templates.TemplateResponse(
        "about.html",
        {
            "request": request,
            "tag": 'about',
        },
    )

@router.post("/")
def def_calculator(request: Request, req: DEF = Depends()):
    print(req)

    atk = req.atk
    spell = req.spell
    stat_bonus = req.stat_bonus
    psy_bonus = req.psy_bonus
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
    dmg_taken = ((1-norm_dmg/((atk-defence*(1-def_redn/100))*(norm_pow/100)*(1+spell/100))+(stat_bonus+psy_bonus-buff)/100)*100)

    return templates.TemplateResponse(
        "def_calculator.html",
        {
            "request": request,
            'data': req,
            "tag": 'def',
            "def": round(defence),
            "dmg_taken": round(dmg_taken),
        },
    )
