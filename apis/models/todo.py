from pydantic import BaseModel


class TaskRequest(BaseModel):
    title: str
    done: bool
    colour: str


class TaskResponse(BaseModel):
    id: str
    title: str
    done: bool
    colour: str


class UpdateTaskRequest(BaseModel):
    title: str | None = None
    done: bool | None = None
    colour: str | None = None
