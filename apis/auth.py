from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from .models.auth import Token, User
from core.auth import AuthCore
from data import Config
import uuid

router = APIRouter()

@router.post("/register", status_code=201, response_model=User)
def register(form_data: OAuth2PasswordRequestForm = Depends()):
    if Config.ENABLE_REGISTRATIONS:
        user_db = AuthCore.file_operations("read")
        if form_data.username in user_db:
            raise HTTPException(status_code=400, detail="Username already registered")
        user_db[form_data.username] = {
            "username": form_data.username,
            "hashed_password": AuthCore.hash_password(form_data.password),
            "id": str(uuid.uuid4()),
            "disabled": False,
        }
        AuthCore.file_operations("write", user_db)
        return User(username=form_data.username, id=user_db[form_data.username]["id"], disabled=user_db[form_data.username]["disabled"])
    else:
        raise HTTPException(status_code=400, detail="Registrations are disabled")


@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = AuthCore.authenticate_user(
        AuthCore.file_operations("read"), form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = AuthCore.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=User)
def get_current_user(current_user: User = Depends(AuthCore.get_current_active_user)):
    return current_user


@router.get("/users/me/id")
def get_current_user_id(current_user: User = Depends(AuthCore.get_current_active_user)):
    return {"id": current_user.id}
