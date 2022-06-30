import os
import sys

from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import Config, app

Config.ENCRYPT_JSON = 1
Config.DATA_DIR = "tests/data_encrypted"


with TestClient(app) as client:

    def test_read_all_todos_no_auth(set_env_vars_encrypted):
        response = client.get("/api/todo/")
        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}

    def login():
        response = client.post(
            "/api/auth/token", data={"username": "pytest", "password": "pytest"}
        )
        return response.json()["access_token"]

    def test_create_todo(set_env_vars_encrypted):
        access_token = login()
        response = client.post(
            "/api/todo/",
            json={"title": "test", "done": False, "colour": "red"},
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 201
        assert response.json() == {
            "title": "test",
            "done": False,
            "colour": "red",
            "id": response.json()["id"],
            "created_at": response.json()["created_at"],
            "updated_at": response.json()["updated_at"],
        }
        global id
        id = response.json()["id"]

    def test_update_todo(set_env_vars_encrypted):
        access_token = login()
        response = client.put(
            f"/api/todo/{id}",
            json={"title": "test2", "done": True, "colour": "blue"},
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 200
        assert response.json() == {
            "title": "test2",
            "done": True,
            "colour": "blue",
            "id": id,
            "created_at": response.json()["created_at"],
            "updated_at": response.json()["updated_at"],
        }

    def test_read_todo(set_env_vars_encrypted):
        access_token = login()
        response = client.get(
            f"/api/todo/{id}", headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == 200
        assert response.json() == {
            "title": "test2",
            "done": True,
            "colour": "blue",
            "id": id,
            "created_at": response.json()["created_at"],
            "updated_at": response.json()["updated_at"],
        }

    def test_read_all_todos(set_env_vars_encrypted):
        access_token = login()
        response = client.get(
            "/api/todo/", headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == 200
        assert response.json() == {
            id: {
                "id": id,
                "title": "test2",
                "done": True,
                "colour": "blue",
                "created_at": response.json()[id]["created_at"],
                "updated_at": response.json()[id]["updated_at"],
            }
        }

    def test_read_all_todos_with_cookie(set_env_vars_encrypted):
        access_token = login()
        cookies = {"Authorization": f"Bearer {access_token}"}
        response = client.get(
            "/api/todo/", cookies=cookies
        )
        assert response.status_code == 200
        assert response.json() == {
            id: {
                "id": id,
                "title": "test2",
                "done": True,
                "colour": "blue",
                "created_at": response.json()[id]["created_at"],
                "updated_at": response.json()[id]["updated_at"],
            }
        }

    def test_delete_todo(set_env_vars_encrypted):
        access_token = login()
        response = client.delete(
            f"/api/todo/{id}", headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == 200
        assert response.json() == {"message": "Task deleted"}

    def test_update_todo_not_found(set_env_vars_encrypted):
        access_token = login()
        response = client.put(
            "/api/todo/test",
            json={"title": "test2", "done": True, "colour": "blue"},
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 404
        assert response.json() == {"detail": "Task not found"}

    def test_delete_todo_not_found(set_env_vars_encrypted):
        access_token = login()
        response = client.delete(
            "/api/todo/test", headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == 404
        assert response.json() == {"detail": "Task not found"}

    def test_read_todo_not_found(set_env_vars_encrypted):
        access_token = login()
        response = client.get(
            "/api/todo/test", headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == 404
        assert response.json() == {"detail": "Task not found"}
