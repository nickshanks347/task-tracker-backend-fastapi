from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from core.config import Config
from core.db import crud
from core.db.database import SessionLocal

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

    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        to_encode.update({"iat": datetime.utcnow()})
        encoded_jwt = jwt.encode(
            to_encode, Config.JWT_SECRET_KEY, algorithm=Config.ALGORITHM
        )
        return encoded_jwt

    def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token, Config.JWT_SECRET_KEY, algorithms=[Config.ALGORITHM]
            )
            username: str = payload.get("sub")
        except (ExpiredSignatureError, JWTError):
            raise credentials_exception
        user = crud.get_user(db, username=username)
        return user
