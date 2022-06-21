from pydantic import BaseModel


class TaskRequest(BaseModel):
    title: str
    done: bool
    colour: str
    
class TaskResponse(TaskRequest):
    id: str
    created_at: str
    updated_at: str

class UpdateTaskRequest(BaseModel):
    title: str | None = None
    done: bool | None = None
    colour: str | None = None
    id: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
