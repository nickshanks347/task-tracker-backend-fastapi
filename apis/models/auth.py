from pydantic import BaseModel
from typing import Union


class User(BaseModel):
    username: str
    id: str
    disabled: Union[bool, None]


class UserInDB(User):
    hashed_password: Union[str, None]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None]
