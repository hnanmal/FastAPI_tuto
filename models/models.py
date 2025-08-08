from __future__ import annotations
from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """
    SQLAlchemy ORM 모델의 기본(Base) 클래스.

    모든 ORM 모델은 이 클래스를 상속받아야 하며,
    이를 통해 동일한 메타데이터 객체를 공유하고
    테이블 생성 및 마이그레이션 시 일관성을 유지합니다.
    """

    pass


class UserModel(Base):
    """
    사용자(User)를 나타내는 SQLAlchemy ORM 모델.

    속성:
        id (int): 기본 키. 각 사용자를 구분하는 고유 ID.
        name (str): 사용자 이름. 유일해야 함.
        todos (list[TodoModel]): 해당 사용자가 소유한 Todo 목록.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, doc="기본 키: 사용자의 고유 ID"
    )
    name: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, doc="사용자 이름(고유해야 함)"
    )

    todos: Mapped[list["TodoModel"]] = relationship(
        back_populates="owner",
        cascade="all, delete-orphan",
        doc="이 사용자가 소유한 TodoModel 객체 리스트",
    )


class TodoModel(Base):
    """
    할 일(Todo)을 나타내는 SQLAlchemy ORM 모델.

    속성:
        id (int): 기본 키. 각 Todo를 구분하는 고유 ID.
        title (str): 할 일 제목 또는 간단한 설명.
        completed (bool): 완료 여부.
        user_id (int | None): 소유한 사용자(User)의 외래 키. 없을 경우 NULL.
        owner (UserModel | None): 이 Todo를 소유한 사용자 객체.
    """

    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, doc="기본 키: Todo의 고유 ID"
    )
    title: Mapped[str] = mapped_column(String(255), doc="할 일 제목 또는 간단한 설명")
    completed: Mapped[bool] = mapped_column(
        Boolean, default=False, doc="할 일 완료 여부. 기본값 False"
    )

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        doc="users.id를 참조하는 외래 키. 할당되지 않으면 NULL",
    )
    owner: Mapped["UserModel | None"] = relationship(
        back_populates="todos", doc="이 Todo를 소유한 UserModel 객체"
    )
