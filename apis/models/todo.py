from pydantic import BaseModel


class TaskRequest(BaseModel):
    title: str
    done: bool
    colour: str


class TaskResponse(TaskRequest):
    id: str
    created_at: str
    updated_at: str | None = None


class UpdateTaskRequest(BaseModel):
    title: str | None = None
    done: bool | None = None
    colour: str | None = None