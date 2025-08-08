# app/crud/user.py
from __future__ import annotations
from typing import Optional, List
from sqlalchemy.orm import Session

from models.models import UserModel
from schemas.schemas import UserCreate


def create_user(db: Session, user: UserCreate) -> UserModel:
    """사용자 생성"""
    db_user = UserModel(name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int) -> Optional[UserModel]:
    """ID로 단건 조회"""
    return db.query(UserModel).filter(UserModel.id == user_id).first()


def get_user_by_name(db: Session, name: str) -> Optional[UserModel]:
    """이름으로 단건 조회 (중복 체크 등에 활용)"""
    return db.query(UserModel).filter(UserModel.name == name).first()


def get_all_users(db: Session) -> List[UserModel]:
    """전체 사용자 목록"""
    return db.query(UserModel).all()


def update_user_name(db: Session, user_id: int, new_name: str) -> Optional[UserModel]:
    """사용자 이름 변경"""
    user = get_user(db, user_id)
    if not user:
        return None
    user.name = new_name
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> bool:
    """사용자 삭제. 삭제 성공 시 True, 대상 없으면 False"""
    user = get_user(db, user_id)
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True
