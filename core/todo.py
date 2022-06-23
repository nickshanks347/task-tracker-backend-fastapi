import uuid
import json
from json import JSONDecodeError
from pathlib import Path
from fastapi import HTTPException
import datetime
from cryptography.fernet import Fernet
from data import Config
import base64


class TodoCore(object):
    task_not_found = HTTPException(status_code=404, detail="Task not found")
    incorrect_format = HTTPException(
        status_code=404, detail="Incorrect tasks JSON format"
    )
    def file_operations(current_user, operation, data=None):
        key = base64.urlsafe_b64encode(Config.JSON_SECRET_KEY.encode())
        fernet = Fernet(key)
        try:
            with open(
                Path(__file__).parent.parent / "data" / f"{current_user.id}.json", "rb+"
            ) as f:
                if operation == "read":
                    data = f.read().decode()
                    data = json.loads(data)["encrypted"]
                    decrypted = fernet.decrypt(data.encode()).decode()
                    return json.loads(decrypted)
                else:
                    f.seek(0)
                    encrypted = json.dumps(data).encode()
                    encrypted = fernet.encrypt(encrypted).decode()
                    print(encrypted)
                    write = {"encrypted": encrypted}
                    f.write(json.dumps(write).encode())
                    f.truncate()
                    f.close()
                    return True
        except JSONDecodeError:
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
        todos = TodoCore.file_operations(current_user, "read")
        task = todos[id]
        return task

    def update_todo(id, body, current_user):
        todos = TodoCore.file_operations(current_user, "read")
        todo = todos[id]
        for k, v in body:
            if v is not None:
                todo[k] = v
        todo["updated_at"] = str(datetime.datetime.now())
        todos[id] = todo
        TodoCore.file_operations(current_user, "write", todos)
        return todo

    def delete_todo(id, current_user):
        todos = TodoCore.file_operations(current_user, "read")
        del todos[id]
        TodoCore.file_operations(current_user, "write", todos)
        return {"message": "Task deleted"}
