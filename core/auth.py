from datetime import datetime, timedelta
import json
from pathlib import Path
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from apis.models.auth import User, TokenData, UserInDB

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class AuthCore(object):
    def get_user_db():
        with open(Path(__file__).parent.parent / "data" / "users.json", "r") as f:
            return json.load(f)

    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

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
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def get_user(db, username: str):
        if username in db:
            user_dict = db[username]
            return UserInDB(**user_dict)

    def get_current_user(token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        user = AuthCore.get_user(AuthCore.get_user_db(), username=token_data.username)
        if user is None:
            raise credentials_exception
        return user

    def get_current_active_user(current_user: User = Depends(get_current_user)):
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user
