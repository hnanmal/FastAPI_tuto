from __future__ import annotations

from typing import List  # 필요시
from pydantic import BaseModel, ConfigDict

from domain.user.user_schema import UserOut


# -------- Todo --------
class TodoCreate(BaseModel):
    """요청용"""

    title: str
    user_id: int | None  # Optional[int] == int | None


class TodoOut(BaseModel):
    """응답용"""

    id: int
    title: str
    completed: bool
    owner: UserOut | None  # 연결된 User 포함

    # Pydantic v2
    model_config = ConfigDict(from_attributes=True)


class TodoUpdate(BaseModel):
    title: str
    completed: bool


class TodoPatch(BaseModel):
    title: str | None = None
    completed: bool | None = None
    user_id: int | None = None
