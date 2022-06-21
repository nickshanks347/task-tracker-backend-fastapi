import uuid
import json
from json import JSONDecodeError
from pathlib import Path
from fastapi import HTTPException
import datetime

class TodoCore(object):
    task_not_found = HTTPException(status_code=404, detail="Task not found")
    incorrect_format = HTTPException(status_code=404, detail="Incorrect tasks JSON format")

    def get_all_todos(current_user):
        try:
            with open(Path(__file__).parent.parent / 'data' / f'{current_user.id}.json', 'r') as f:
                todos = json.load(f)
        except JSONDecodeError:
            raise TodoCore.incorrect_format
        except: 
            raise HTTPException(status_code=404, detail="No tasks found")
        return todos

    def create_todo(task, current_user):
        try:
            with open(Path(__file__).parent.parent / 'data' / f'{current_user.id}.json', 'r+') as f:
                todos = json.load(f)
                id = str(uuid.uuid4())
                created_at = str(datetime.datetime.now())
                updated_at = str(datetime.datetime.now())
                task = {"id": id, "title": task.title, "done": task.done, "colour": task.colour, "created_at": created_at, "updated_at": updated_at}
                todos[id] = task
                f.seek(0)
                json.dump(todos, f, indent=4)
                f.truncate()
                f.close()
                return task
        except JSONDecodeError:
            raise TodoCore.incorrect_format

    def get_todo(id, current_user):
        try:
            with open(Path(__file__).parent.parent / 'data' / f'{current_user.id}.json', 'r') as f:
                todos = json.load(f)
            task = todos[id]
            return task
        except JSONDecodeError:
            raise TodoCore.incorrect_format
        except:
            raise TodoCore.task_not_found

    def update_todo(id, body, current_user):
        try:
            with open(Path(__file__).parent.parent / 'data' / f'{current_user.id}.json', 'r+') as f:
                user_file = json.load(f)
                todo = user_file[id]
                for k, v in body:
                    if v is not None:
                        todo[k] = v
                todo["updated_at"] = str(datetime.datetime.now())
                user_file[id] = todo
                f.seek(0)
                json.dump(user_file, f, indent=4)
                f.truncate()
                f.close()
                return todo  
        except JSONDecodeError:
            raise TodoCore.incorrect_format
        except:
            raise TodoCore.task_not_found

    def delete_todo(id, current_user):
        try:
            with open(Path(__file__).parent.parent / 'data' / f'{current_user.id}.json', 'r+') as f:
                user_file = json.load(f)
                del user_file[id]
                f.seek(0)
                json.dump(user_file, f, indent=4)
                f.truncate()
                f.close()
                return {"message": "Task deleted"}
        except JSONDecodeError:
            raise TodoCore.incorrect_format
        except:
            raise TodoCore.task_not_found