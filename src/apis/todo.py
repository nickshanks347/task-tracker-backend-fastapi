from core.auth import AuthCore
from fastapi import APIRouter, Depends, HTTPException

from core.db.schemas import Todo, User
from core.db.schemas import TodoBase, TodoCreate, TodoUpdate
from core.db import crud, models, schemas
from core.db.database import SessionLocal, engine
from sqlalchemy.orm import Session

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_all_todos(current_user: User = Depends(AuthCore.get_current_user), db: Session = Depends(get_db)):
    return crud.get_todos(db, current_user.id)


@router.post("/", response_model=TodoCreate)
def create_todo(todo: TodoBase, current_user: User = Depends(AuthCore.get_current_user), db: Session = Depends(get_db)):
    return crud.create_todo(db, todo=todo, user_id=current_user.id)


@router.get("/{id}", response_model=Todo)
def get_todo(id: str, current_user: User = Depends(AuthCore.get_current_user), db: Session = Depends(get_db)):
    todo = crud.get_todo(db, current_user.id, id)
    if todo:
        return todo
    else:
        raise HTTPException(status_code=404, detail="Todo not found")


@router.post("/{id}", response_model=TodoUpdate)
def update_todo(id: str, todo: TodoBase, current_user: User = Depends(AuthCore.get_current_user), db: Session = Depends(get_db)):
    return crud.update_todo(db, id=id, todo=todo, user_id=current_user.id)


@router.delete("/{id}")
def delete_todo(id: str, current_user: User = Depends(AuthCore.get_current_user), db: Session = Depends(get_db)):
    crud.delete_todo(db, id=id, user_id=current_user.id)
    return {"message": "Todo deleted"}