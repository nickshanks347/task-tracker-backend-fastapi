from datetime import datetime, timedelta


from core.db.schemas import TokenData, UserCreate
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from core.db.database import SessionLocal

from core.config import Config
from core.db import crud

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class AuthCore(object):
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def hash_password(plain_password):
        return pwd_context.hash(plain_password)

    def authenticate_user(user_db, username: str, password: str):
        user = AuthCore.get_user(user_db, username)
        if not user:
            return False
        if not AuthCore.verify_password(password, user.hashed_password):
            return False
        return user

    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        to_encode.update({"iat": datetime.utcnow()})
        encoded_jwt = jwt.encode(
            to_encode, Config.JWT_SECRET_KEY, algorithm=Config.ALGORITHM
        )
        return encoded_jwt

    def get_user(db, username: str):
        if username in db:
            user_dict = db[username]
            return UserCreate(**user_dict)

    def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        token_expired = HTTPException(
            status_code=401,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token, Config.JWT_SECRET_KEY, algorithms=[Config.ALGORITHM]
            )
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except ExpiredSignatureError:
            raise token_expired
        except JWTError:
            raise credentials_exception
        user = crud.get_user(db, username=username)
        if user is None:
            raise credentials_exception
        return user
