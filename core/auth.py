from datetime import datetime, timedelta
from json import JSONDecodeError
from pathlib import Path
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from apis.models.auth import User, TokenData, UserInDB
from data import Config
from .fileops import FileOps

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthCore(object):
    def file_operations(operation, data=None):
        try:
            with open(Path(__file__).parent.parent / "data" / "users.json", "rb+") as f:   
                return FileOps.file_operations_encrypted(operation, f, data) if Config.ENCRYPT_JSON else FileOps.file_operations_plain(operation, f, data)
        except JSONDecodeError:
            raise AuthCore.incorrect_format

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
        encoded_jwt = jwt.encode(to_encode, Config.JWT_SECRET_KEY, algorithm=Config.ALGORITHM)
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
            payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=[Config.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        user = AuthCore.get_user(AuthCore.file_operations("read"), username=token_data.username)
        if user is None:
            raise credentials_exception
        return user

    def get_current_active_user(current_user: User = Depends(get_current_user)):
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user
