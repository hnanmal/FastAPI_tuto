from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class TodoModel(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    completed = Column(Boolean, default=False)
