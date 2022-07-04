from fastapi.testclient import TestClient
from main import app


with TestClient(app) as client:

    def login():
        response = client.post("/api/auth/login", data={"username": "pytest", "password": "pytest"})
        return response.json()["access_token"]

    def test_create_todo():
        access_token = login()
        response = client.post("/api/todo/", json={"title": "pytest", "done": False, "colour": "red"}, headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 201
        assert response.json() == {"title": "pytest", "done": False, "colour": "red", "id": response.json()["id"], "created_at": response.json()["created_at"]}
        global id
        id = response.json()["id"]

    def test_update_todo():
        access_token = login()
        response = client.put(f"/api/todo/{id}", json={"title": "pytest_updated", "done": True, "colour": "blue"}, headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 200
        assert response.json() == {"title": "pytest_updated", "done": True, "colour": "blue", "created_at": response.json()["created_at"], "updated_at": response.json()["updated_at"]}

    def test_get_todo():
        access_token = login()
        response = client.get("/api/todo/" + str(id), headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 200
        assert response.json() == {"title": "pytest_updated", "done": True, "colour": "blue", "id": response.json()["id"], "created_at": response.json()["created_at"], "updated_at": response.json()["updated_at"]}

    def test_create_second_todo():
        access_token = login()
        response = client.post("/api/todo/", json={"title": "pytest2", "done": False, "colour": "red"}, headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 201
        assert response.json() == {"title": "pytest2", "done": False, "colour": "red", "id": response.json()["id"], "created_at": response.json()["created_at"]}

    def test_get_todos():
        access_token = login()
        response = client.get("/api/todo/", headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 200
        assert response.json() == [{"title": "pytest_updated", "done": True, "colour": "blue", "id": response.json()[0]["id"], "created_at": response.json()[0]["created_at"], "updated_at": response.json()[0]["updated_at"]}, {"title": "pytest2", "done": False, "colour": "red", "id": response.json()[1]["id"], "created_at": response.json()[1]["created_at"], "updated_at": response.json()[1]["updated_at"]}]

    def test_delete_todo():
        access_token = login()
        response = client.delete("/api/todo/" + str(id), headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 200
        assert response.json() == {"message": "Todo deleted"}

    def test_get_todo_not_found():
        access_token = login()
        response = client.get("/api/todo/" + str(id), headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 404
        assert response.json() == {"detail": "Todo not found"}

    def test_delete_todo_not_found():
        access_token = login()
        response = client.delete("/api/todo/" + str(id), headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 404
        assert response.json() == {"detail": "Todo not found"}

    def test_update_todo_not_found():
        access_token = login()
        response = client.put("/api/todo/" + str(id), json={"title": "pytest_updated", "done": False, "colour": "red"}, headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 404
        assert response.json() == {"detail": "Todo not found"}
