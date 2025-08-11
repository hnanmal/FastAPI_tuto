from __future__ import annotations

from typing import List  # 필요시
from pydantic import BaseModel, ConfigDict


# -------- User --------
class UserCreate(BaseModel):
    name: str


class UserOut(BaseModel):
    id: int
    name: str

    # Pydantic v2: orm_mode -> from_attributes
    model_config = ConfigDict(from_attributes=True)
