import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
    id = str(uuid.uuid4())
    db_user = models.User(username=user.username, id=id, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_todos(db: Session, user_id: str):
    return db.query(models.Todo).filter(models.Todo.owner_id == user_id).all()


def get_todo(db: Session, user_id: str, id: str):
    return db.query(models.Todo).filter(models.Todo.id == id, models.Todo.owner_id == user_id).first()


def create_todo(db: Session, todo: schemas.TodoCreate, user_id: int):
    id = str(uuid.uuid4())
    db_todo = models.Todo(id=id, title=todo.title, done=todo.done, colour=todo.colour, owner_id=user_id, created_at=datetime.now())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def update_todo(db: Session, id: int, todo: schemas.TodoUpdate, user_id: int):
    db_todo = db.query(models.Todo).filter(models.Todo.id == id, models.Todo.owner_id == user_id).first()
    if db_todo:
        db_todo.title = todo.title
        db_todo.done = todo.done
        db_todo.colour = todo.colour
        db_todo.updated_at = datetime.now()
        db.commit()
        db.refresh(db_todo)
        return db_todo
    return None


def delete_todo(db: Session, id: int, user_id: int):
    db_todo = db.query(models.Todo).filter(models.Todo.id == id, models.Todo.owner_id == user_id).first()
    if db_todo:
        db.delete(db_todo)
        db.commit()
        return db_todo
    return None
