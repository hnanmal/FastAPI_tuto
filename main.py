from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import init_db
from routers import todo, user

app = FastAPI()

# DB 초기화
init_db()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(todo.router)
app.include_router(user.router)
