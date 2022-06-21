import uuid
from fastapi import HTTPException

todos = []
todos.append({"id": "1", "title": "Task 1", "done": False, "colour": "red"})
todos.append({"id": "2", "title": "Task 2", "done": False, "colour": "blue"})
todos.append({"id": "3", "title": "Task 3", "done": False, "colour": "green"})


class TodoCore(object):
    def get_all_todos():
        return todos

    def create_todo(task):
        id = str(uuid.uuid4())
        task = {"id": id, "title": task.title, "done": task.done, "colour": task.colour}
        todos.append(task)
        return task

    def get_todo(id):
        for todo in todos:
            if todo["id"] == id:
                return todo
        raise HTTPException(status_code=404, detail="Task not found")

    def update_todo(id, task):
        for todo in todos:
            if todo["id"] == id:
                for k, v in task:
                    if v is not None:
                        todo[k] = v
                return todo
        raise HTTPException(status_code=404, detail="Task not found")

    def delete_todo(id):
        for todo in todos:
            if todo["id"] == id:
                todos.remove(todo)
                return {"message": "Task deleted"}
        raise HTTPException(status_code=404, detail="Task not found")
