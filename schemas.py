from pydantic import BaseModel
from typing import Optional


class TodoCreate(BaseModel):
    """요청용"""

    title: str


class TodoOut(BaseModel):
    """응답용"""

    id: int
    title: str
    completed: bool

    class Config:
        orm_mode = True  # SQLAlchemy 모델 -> 자동 변환 가능


class TodoUpdate(BaseModel):
    title: str
    completed: bool


class TodoPatch(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None
