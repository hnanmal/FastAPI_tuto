from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

import crud.todo
from dependencies.deps import get_db
from models.models import TodoModel
from schemas.schemas import TodoCreate, TodoOut, TodoPatch, TodoUpdate


router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("/", response_model=TodoOut)
def create(todo: TodoCreate, db: Session = Depends(get_db)):
    return crud.todo.create_todo(db, todo)


@router.get("/", response_model=List[TodoOut])
def read_all(db: Session = Depends(get_db)):
    return db.query(TodoModel).options(joinedload(TodoModel.owner)).all()


@router.put("/{todo_id}", response_model=TodoOut)
def update(todo_id: int, update_data: TodoUpdate, db: Session = Depends(get_db)):
    todo = crud.todo.update_todo(db, todo_id, update_data)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.patch("/{todo_id}", response_model=TodoOut)
def patch(todo_id: int, update_data: TodoPatch, db: Session = Depends(get_db)):
    todo = crud.todo.patch_todo(db, todo_id, update_data)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.delete("/{todo_id}")
def delete(todo_id: int, db: Session = Depends(get_db)):
    crud.todo.delete_todo(db, todo_id)
    return {"message": f"Todo {todo_id} deleted"}
