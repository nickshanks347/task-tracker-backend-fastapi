from datetime import timedelta

from core.auth import AuthCore
from core.config import Config
from core.db import crud
from core.db.database import SessionLocal
from core.db.schemas import Token, User, UserBase, UserId
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=UserBase)
def register(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db), disabled: bool = False):
    user = crud.get_user(db, form_data.username)
    if not Config.ENABLE_REGISTRATIONS:
        raise HTTPException(status_code=400, detail="Registrations are disabled")
    if user:
        raise HTTPException(status_code=400, detail="User already registered")
    hashed_password = AuthCore.hash_password(form_data.password)
    user = crud.create_user(db, form_data, hashed_password, disabled)
    return user


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user(db, form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not AuthCore.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    if user.disabled:
        raise HTTPException(status_code=401, detail="User is disabled")
    access_token = AuthCore.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=UserBase)
def get_user(current_user: User = Depends(AuthCore.get_current_user)):
    return current_user


@router.get("/users/me/id", response_model=UserId)
def get_user_id(current_user: User = Depends(AuthCore.get_current_user)):
    return current_user
