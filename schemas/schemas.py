from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    name: str


class UserOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class TodoCreate(BaseModel):
    """요청용"""

    title: str
    user_id: Optional[int]  # 🔥 user_id 받을 수 있게 함


class TodoOut(BaseModel):
    """응답용"""

    id: int
    title: str
    completed: bool
    owner: Optional[UserOut]  # 연결된 User 포함

    class Config:
        orm_mode = True  # SQLAlchemy 모델 -> 자동 변환 가능


class TodoUpdate(BaseModel):
    title: str
    completed: bool


class TodoPatch(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None
    user_id: Optional[int] = None
