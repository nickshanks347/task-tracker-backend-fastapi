import uuid
from json import JSONDecodeError
from pathlib import Path
from fastapi import HTTPException
import datetime
from data import Config
from .fileops import FileOps


class TodoCore(object):
    task_not_found = HTTPException(status_code=404, detail="Task not found")
    incorrect_format = HTTPException(
        status_code=404, detail="Tasks JSON file has wrong format or does not exist"
    )

    def file_operations(current_user, operation, data=None):
        try:
            if Config.ENCRYPT_JSON:
                with open(
                    Path(__file__).parent.parent / "data" / f"{current_user.id}.json",
                    "rb+",
                ) as f:
                    return FileOps.file_operations_encrypted(operation, f, data)
            else:
                with open(
                    Path(__file__).parent.parent / "data" / f"{current_user.id}.json",
                    "r+",
                ) as f:
                    return FileOps.file_operations_plain(operation, f, data)
        except JSONDecodeError:
            raise TodoCore.incorrect_format
        except FileNotFoundError:
            raise TodoCore.incorrect_format

    def get_all_todos(current_user):
        todos = TodoCore.file_operations(current_user, "read")
        return todos

    def create_todo(task, current_user):
        todos = TodoCore.file_operations(current_user, "read")
        id = str(uuid.uuid4())
        created_at = str(datetime.datetime.now())
        task = {
            "id": id,
            "title": task.title,
            "done": task.done,
            "colour": task.colour,
            "created_at": created_at,
            "updated_at": None,
        }
        todos[id] = task
        TodoCore.file_operations(current_user, "write", todos)
        return task

    def get_todo(id, current_user):
        try:
            todos = TodoCore.file_operations(current_user, "read")
            task = todos[id]
            return task
        except KeyError:
            raise TodoCore.task_not_found

    def update_todo(id, body, current_user):
        try:
            todos = TodoCore.file_operations(current_user, "read")
            todo = todos[id]
            for k, v in body:
                if v is not None:
                    todo[k] = v
            todo["updated_at"] = str(datetime.datetime.now())
            todos[id] = todo
            TodoCore.file_operations(current_user, "write", todos)
            return todo
        except KeyError:
            raise TodoCore.task_not_found

    def delete_todo(id, current_user):
        try:
            todos = TodoCore.file_operations(current_user, "read")
            del todos[id]
            TodoCore.file_operations(current_user, "write", todos)
            return {"message": "Task deleted"}
        except KeyError:
            raise TodoCore.task_not_found
