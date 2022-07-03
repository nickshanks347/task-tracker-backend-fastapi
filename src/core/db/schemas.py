from pydantic import BaseModel


class TodoBase(BaseModel):
    title: str
    done: bool
    colour: str


class TodoCreate(TodoBase):
    id: str
    created_at: str

    class Config:
        orm_mode = True


class TodoUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None
    colour: str | None = None
    created_at: str | None = None
    updated_at: str | None = None

    class Config:
        orm_mode = True


class Todo(TodoBase):
    title: str
    done: bool
    colour: str
    id: str
    created_at: str
    updated_at: str | None = None

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    id: str
    disabled: bool | None = None

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    hashed_password: str


class UserId(BaseModel):
    id: str

    class Config:
        orm_mode = True


class User(UserBase):
    username: str
    hashed_password: str
    id: str
    disabled: bool | None = None

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
