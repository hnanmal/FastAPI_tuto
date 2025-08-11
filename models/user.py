from __future__ import annotations
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

# from models.todo import TodoModel
from .base import Base


class UserModel(Base):
    """
    사용자(User)를 나타내는 ORM 모델.

    속성:
        id (int): 기본 키(고유 ID)
        name (str): 사용자 이름(유일)
        todos (list[TodoModel]): 사용자가 소유한 Todo 목록
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, doc="기본 키: 사용자의 고유 ID"
    )
    name: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, doc="사용자 이름(고유)"
    )

    todos: Mapped[list["TodoModel"]] = relationship(
        back_populates="owner",
        cascade="all, delete-orphan",
        doc="이 사용자가 소유한 TodoModel 리스트",
    )
