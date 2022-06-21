from pydantic import BaseModel


class User(BaseModel):
    username: str
    id: str
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
