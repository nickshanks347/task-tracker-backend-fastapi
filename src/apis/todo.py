from typing import List
from core.auth import AuthCore
from core.db import crud
from core.db.database import SessionLocal
from core.db.schemas import Todo, TodoBase, TodoCreate, TodoUpdate, User
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[Todo])
def get_all_todos(current_user: User = Depends(AuthCore.get_current_user), db: Session = Depends(get_db)):
    return crud.get_todos(db, current_user.id)


@router.post("/", response_model=TodoCreate, status_code=201)
def create_todo(todo: TodoBase, current_user: User = Depends(AuthCore.get_current_user), db: Session = Depends(get_db)):
    return crud.create_todo(db, todo=todo, user_id=current_user.id)


@router.get("/{id}", response_model=Todo)
def get_todo(id: str, current_user: User = Depends(AuthCore.get_current_user), db: Session = Depends(get_db)):
    todo = crud.get_todo(db, current_user.id, id)
    if todo:
        return todo
    else:
        raise HTTPException(status_code=404, detail="Todo not found")


@router.put("/{id}", response_model=TodoUpdate)
def update_todo(id: str, todo: TodoBase, current_user: User = Depends(AuthCore.get_current_user), db: Session = Depends(get_db)):
    todo = crud.update_todo(db, id=id, todo=todo, user_id=current_user.id)
    if todo:
        return todo
    else:
        raise HTTPException(status_code=404, detail="Todo not found")


@router.delete("/{id}", responses={200: {"description": "Todo deleted", "content": {"application/json": {"example": {"message": "Task deleted"}}}}})
def delete_todo(id: str, current_user: User = Depends(AuthCore.get_current_user), db: Session = Depends(get_db)):
    todo = crud.delete_todo(db, id=id, user_id=current_user.id)
    if todo:
        return {"message": "Todo deleted"}
    else:
        raise HTTPException(status_code=404, detail="Todo not found")
