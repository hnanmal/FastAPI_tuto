from __future__ import annotations
from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

# from models.user import UserModel
from .base import Base


class TodoModel(Base):
    """
    할 일(Todo) ORM 모델.

    속성:
        id (int): 기본 키
        title (str): 제목/간단 설명
        completed (bool): 완료 여부
        user_id (int | None): 소유 사용자 FK (없을 수 있음)
        owner (UserModel | None): 소유한 사용자 객체
    """

    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        doc="기본 키: Todo의 고유 ID",
    )
    title: Mapped[str] = mapped_column(
        String(255),
        doc="할 일 제목 또는 간단한 설명",
    )
    completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        doc="완료 여부(기본 False)",
    )

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        doc="users.id 참조 FK. 미할당 시 NULL",
    )
    owner: Mapped["UserModel | None"] = relationship(
        back_populates="todos",
        doc="이 Todo를 소유한 UserModel",
    )
