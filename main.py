from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import init_db
from domain.user import user_router
from domain.todo import todo_router

app = FastAPI()

# DB 초기화
init_db()

# CORS 설정
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(todo_router.router)
app.include_router(user_router.router)
