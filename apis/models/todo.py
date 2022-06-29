from pydantic import BaseModel
from typing import Union


class TaskRequest(BaseModel):
    title: str
    done: bool
    colour: str


class TaskResponse(TaskRequest):
    id: str
    created_at: str
    updated_at: Union[str, None]


class UpdateTaskRequest(BaseModel):
    title: Union[str, None]
    done: Union[bool, None]
    colour: Union[str, None]
