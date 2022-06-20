from fastapi import APIRouter, Response
import uuid
from pydantic import BaseModel

router = APIRouter()


class Task(BaseModel):
    title: str
    done: bool
    colour: str


class TaskResponse(BaseModel):
    id: str
    title: str
    done: bool
    colour: str


class UpdateTask(BaseModel):
    title: str | None = None
    done: bool | None = None
    colour: str | None = None


todos = []
todos.append({"id": "1", "title": "Task 1", "done": False, "colour": "red"})
todos.append({"id": "2", "title": "Task 2", "done": False, "colour": "blue"})
todos.append({"id": "3", "title": "Task 3", "done": False, "colour": "green"})


@router.get(
    "/",
    status_code=200,
    responses={200: {"description": "Success", "model": TaskResponse}},
)
def get_all_todos():
    return todos


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=201,
    responses={201: {"description": "Created", "model": TaskResponse}},
)
def create_todo(task: Task):
    id = str(uuid.uuid4())
    task = {"id": id, "title": task.title, "done": task.done, "colour": task.colour}
    todos.append(task)
    return task


@router.post(
    "/{id}",
    status_code=200,
    responses={
        404: {"description": "Task not found"},
        200: {"description": "Successful", "model": TaskResponse},
    },
)
def get_todo(id: str, response: Response):
    for todo in todos:
        if todo["id"] == id:
            return todo
    response.status_code = 404
    return {"error": "Task not found"}


@router.put(
    "/{id}",
    response_model=TaskResponse,
    status_code=200,
    responses={
        404: {"description": "Task not found"},
        200: {"description": "Updated", "model": TaskResponse},
    },
)
def update_todo(id: str, task: UpdateTask, response: Response):
    for todo in todos:
        if todo["id"] == id:
            for k, v in task:
                if v is not None:
                    todo[k] = v
            return todo
    response.status_code = 404
    return {"error": "Task not found"}


@router.delete(
    "/{id}",
    status_code=200,
    responses={
        404: {"description": "Task not found"},
        200: {"description": "Deleted", "model": TaskResponse},
    },
)
def delete_todo(id: str, response: Response):
    for todo in todos:
        if todo["id"] == id:
            todos.remove(todo)
            return {"message": "Task deleted"}
    response.status_code = 404
    return {"error": "Task not found"}
