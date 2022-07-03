from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    username = Column(String, unique=True, index=True)
    id = Column(String, primary_key=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    todos = relationship("Todo", back_populates="owner")


class Todo(Base):
    __tablename__ = "todos"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    colour = Column(String, index=True)
    done = Column(Boolean, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(String, index=True)
    updated_at = Column(String, index=True, nullable=True)

    owner = relationship("User", back_populates="todos")
