from fastapi import APIRouter, Response
from core.todo import TodoCore
from .models.todo import TaskRequest, TaskResponse, UpdateTaskRequest

router = APIRouter()

@router.get("/", status_code=200, responses={
    200: {"description": "Success", "model": TaskResponse}
    },
)
def get_all_todos():
    return TodoCore.get_all_todos()


@router.post("/", response_model=TaskResponse, status_code=201, responses={
    201: {"description": "Created", "model": TaskResponse}
    },
)
def create_todo(task: TaskRequest):
    return TodoCore.create_todo(task)


@router.post( "/{id}", status_code=200, responses={
        404: {"description": "Task not found"},
        200: {"description": "Successful", "model": TaskResponse},
    },
)
def get_todo(id: str):
    return TodoCore.get_todo(id)


@router.put("/{id}", response_model=TaskResponse, status_code=200, responses={
        404: {"description": "Task not found"},
        200: {"description": "Updated", "model": TaskResponse},
    },
)
def update_todo(id: str, task: UpdateTaskRequest):
    return TodoCore.update_todo(id, task)


@router.delete("/{id}", status_code=200, responses={
        404: {"description": "Task not found"},
        200: {
            "description": "Deleted",
            "content": {"application/json": {"example": {"message": "Task deleted"}}},
        },
    },
)
def delete_todo(id: str):
    return TodoCore.delete_todo(id)
