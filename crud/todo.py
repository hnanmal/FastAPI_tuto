from sqlalchemy.orm import Session
from models.models import TodoModel
from schemas.schemas import TodoCreate, TodoPatch, TodoUpdate


def create_todo(db: Session, todo: TodoCreate):
    db_todo = TodoModel(
        title=todo.title,
        user_id=todo.user_id,
    )  # TodoModel 포맷으로 데이터 생성하고
    db.add(db_todo)  # db에 삽입
    db.commit()
    db.refresh(db_todo)
    return db_todo


def get_all_todos(db: Session):
    # 변경: crud 함수에서 joinedload 없이 기본 쿼리만 반환
    return db.query(TodoModel).all()


def get_todo(db: Session, todo_id: int):
    return db.query(TodoModel).filter(TodoModel.id == todo_id).first()


def update_todo(db: Session, todo_id: int, update_data: TodoUpdate):
    todo = get_todo(db, todo_id)
    if not todo:
        return None
    todo.title = update_data.title
    todo.completed = update_data.completed
    db.commit()
    db.refresh(todo)
    return todo


def patch_todo(db: Session, todo_id: int, update_data: TodoPatch):
    todo = get_todo(db, todo_id)
    if not todo:
        return None
    update_fields = update_data.model_dump(
        exclude_unset=True
    )  # 모델 인스턴스를 dict로 변환
    for key, value in update_fields.items():
        setattr(todo, key, value)
    db.commit()
    db.refresh(todo)
    return todo


def delete_todo(db: Session, todo_id: int):
    todo = get_todo(db, todo_id)
    if todo:
        db.delete(todo)
        db.commit()
