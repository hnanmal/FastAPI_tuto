# app/routers/user.py (발췌)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from dependencies.deps import get_db
from schemas.schemas import UserCreate, UserOut
from crud import user as crud_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # (옵션) 이름 중복 체크
    # if crud_user.get_user_by_name(db, user.name):
    #     raise HTTPException(status_code=400, detail="Name already exists")
    return crud_user.create_user(db, user)


@router.get("/", response_model=List[UserOut])
def read_users(db: Session = Depends(get_db)):
    return crud_user.get_all_users(db)


@router.delete("/{user_id}", status_code=204)
def remove_user(user_id: int, db: Session = Depends(get_db)):
    ok = crud_user.delete_user(db, user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")
    return
