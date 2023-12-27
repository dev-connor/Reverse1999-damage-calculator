from dataclasses import dataclass
from pydantic import BaseModel, Field
from typing import List, Optional
from fastapi import Form

@dataclass
class DEF:
    atk: Optional[int] = Form()
    dmg: Optional[int] = Form()
    spell: Optional[int] = Form()

