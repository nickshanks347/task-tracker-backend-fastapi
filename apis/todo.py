from fastapi import APIRouter, Response, Depends
from core.todo import TodoCore
from core.auth import AuthCore
from .models.todo import TaskRequest, TaskResponse, UpdateTaskRequest
from .models.auth import User

router = APIRouter()

@router.get("/", status_code=200, responses={200: {"description": "Success", "model": TaskResponse}})
def get_all_todos(current_user: User = Depends(AuthCore.get_current_active_user)):
    return TodoCore.get_all_todos(current_user)


@router.post("/", response_model=TaskResponse, status_code=201, responses={201: {"description": "Created", "model": TaskResponse}})
def create_todo(task: TaskRequest, current_user: User = Depends(AuthCore.get_current_active_user)):
    return TodoCore.create_todo(task, current_user)


@router.post( "/{id}", status_code=200, responses={404: {"description": "Task not found"}, 200: {"description": "Successful", "model": TaskResponse},})
def get_todo(id: str, current_user: User = Depends(AuthCore.get_current_active_user)):
    return TodoCore.get_todo(id, current_user)


@router.put("/{id}", response_model=TaskResponse, status_code=200, responses={404: {"description": "Task not found"}, 200: {"description": "Updated", "model": TaskResponse}})
def update_todo(id: str, task: UpdateTaskRequest, current_user: User = Depends(AuthCore.get_current_active_user)):
    return TodoCore.update_todo(id, task, current_user)


@router.delete("/{id}", status_code=200, responses={404: {"description": "Task not found"}, 200: {"description": "Deleted","content": {"application/json": {"example": {"message": "Task deleted"}}},}})
def delete_todo(id: str, current_user: User = Depends(AuthCore.get_current_active_user)):
    return TodoCore.delete_todo(id, current_user)
