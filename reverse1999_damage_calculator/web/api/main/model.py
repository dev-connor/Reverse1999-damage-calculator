from dataclasses import dataclass
from pydantic import BaseModel, Field
from typing import List, Optional
from fastapi import Form

@dataclass
class DEF:
    atk: int = Form()
    bonus: int = Form(0)
    spell: int = Form(0)
    norm_dmg: int = Form()
    pen_dmg: int = Form()
    weakness: bool = Form(False)
    afflatus: bool = Form(False)
    buff: int = Form(0)
    portray: int = Form(0)

@dataclass
class DMG:
    # 아군
    atk: int = Form(0)
    power: int = Form(0)
    stat_bonus: int = Form(0)
    inherit_atk: int = Form(0)
    inherit_bonus: int = Form(0)
    spell: int = Form(0)

    # 적군
    defence: int = Form(0)
    dmg_taken: int = Form(0)
    afflatus: bool = Form(False) # 영감

    # 환경
    def_redn: int = Form(0)
    buff: int = Form(0)
    debuff: int = Form(0)
