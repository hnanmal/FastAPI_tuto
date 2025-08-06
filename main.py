from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import TodoModel, Base, UserModel
from schemas import TodoCreate, TodoOut, TodoPatch, TodoUpdate, UserCreate, UserOut
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from typing import List
from fastapi.middleware.cors import CORSMiddleware


# SQLite DB 연결
DATABASE_URL = "sqlite:///./todo.db"  # 현재 폴더에 items.db 생성
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


# 테이블 생성 (처음 한 번만 실행됨)
Base.metadata.create_all(bind=engine)

# FastAPI 앱 생성
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# DB 세션 의존성 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserModel(name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users/", response_model=List[UserOut])
def read_users(db: Session = Depends(get_db)):
    return db.query(UserModel).all()


@app.post("/todos/", response_model=TodoOut)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = TodoModel(
        title=todo.title, user_id=todo.user_id
    )  # completed는 자동 False
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


@app.get("/todos/", response_model=List[TodoOut])
def read_todos(db: Session = Depends(get_db)):
    # todos = db.query(TodoModel).all()
    todos = db.query(TodoModel).options(joinedload(TodoModel.owner)).all()
    return todos


@app.put("/todos/{todo_id}", response_model=TodoOut)
def update_todo(todo_id: int, update_data: TodoUpdate, db: Session = Depends(get_db)):
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not todo:
        return {"error": "Todo not found"}

    todo.title = update_data.title
    todo.completed = update_data.completed  # 🔥 입력된 값 그대로 적용

    db.commit()
    db.refresh(todo)
    return todo


@app.patch("/todos/{todo_id}", response_model=TodoOut)
def patch_todo(todo_id: int, update_data: TodoPatch, db: Session = Depends(get_db)):
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    update_fields = update_data.model_dump(exclude_unset=True)
    for key, value in update_fields.items():
        setattr(todo, key, value)  # 🔥 필드 자동 업데이트

    db.commit()
    db.refresh(todo)
    return todo


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo)
    db.commit()
    return {"message": f"Todo {todo_id} deleted successfully"}
