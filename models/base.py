from __future__ import annotations
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    SQLAlchemy ORM 모델의 기본(Base) 클래스.
    모든 모델이 이 클래스를 상속받아 동일한 metadata를 공유한다.
    """

    pass
