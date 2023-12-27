from dataclasses import dataclass
from pydantic import BaseModel, Field
from typing import List, Optional
from fastapi import Form

@dataclass
class DEF:
    atk: int = Form()
    bonus: int = Form()
    spell: int = Form()
    norm_dmg: int = Form()
    pen_dmg: int = Form()
    weakness: bool = Form(False)
    afflatus: bool = Form(False)
    buff: Optional[int] = Form()
    portray: int = Form(0)

