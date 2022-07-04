from fastapi.testclient import TestClient
import random
from main import app, Config


def rng():
    return str(random.randint(0, 10000))


class RandomNumber:
    def __init__(self, number):
        self.number = number

    number = rng()


with TestClient(app) as client:

    rn = RandomNumber.number

    def test_registrations_disabled():
        Config.ENABLE_REGISTRATIONS = False
        response = client.post("/api/auth/register", data={"username": "pytest" + rng(), "password": "pytest"})
        assert response.status_code == 400
        assert response.json() == {"detail": "Registrations are disabled"}
        Config.ENABLE_REGISTRATIONS = True

    def test_register_user():
        response = client.post("/api/auth/register", data={"username": "pytest" + rn, "password": "pytest"})
        assert response.status_code == 200
        id = response.json()["id"]
        assert response.json() == {"username": "pytest" + rn, "id": id, "disabled": False}

    def test_register_user_already_exists():
        response = client.post("/api/auth/register", data={"username": "pytest" + rn, "password": "pytest"})
        assert response.status_code == 400
        assert response.json() == {"detail": "User already registered"}

    def test_login_user():
        response = client.post("/api/auth/login", data={"username": "pytest" + rn, "password": "pytest"})
        assert response.status_code == 200
        access_token = response.json()["access_token"]
        assert response.json() == {"access_token": access_token, "token_type": "bearer"}

    def test_login_user_wrong_password():
        response = client.post("/api/auth/login", data={"username": "pytest" + rn, "password": "wrong"})
        assert response.status_code == 400
        assert response.json() == {"detail": "Incorrect username or password"}

    def test_login_user_wrong_username():
        response = client.post("/api/auth/login", data={"username": "wrong" + rn, "password": "pytest"})
        assert response.status_code == 400
        assert response.json() == {"detail": "Incorrect username or password"}

    def test_login_user_disabled():
        response = client.post("/api/auth/register", data={"username": "pytest_disabled" + rn, "password": "pytest"}, params={"disabled": True})
        response = client.post("/api/auth/login", data={"username": "pytest_disabled" + rn, "password": "pytest"})
        assert response.status_code == 401
        assert response.json() == {"detail": "User is disabled"}

    def test_users_me():
        response = client.post("/api/auth/login", data={"username": "pytest" + rn, "password": "pytest"})
        access_token = response.json()["access_token"]
        response = client.get("/api/auth/users/me", headers={"Authorization": f"Bearer {access_token}"})
        id = response.json()["id"]
        assert response.status_code == 200
        assert response.json() == {"username": "pytest" + rn, "id": id, "disabled": False}

    def test_users_me_id():
        response = client.post("/api/auth/login", data={"username": "pytest" + rn, "password": "pytest"})
        access_token = response.json()["access_token"]
        response = client.get("/api/auth/users/me/id", headers={"Authorization": f"Bearer {access_token}"})
        id = response.json()["id"]
        assert response.status_code == 200
        assert response.json() == {"id": id}

    def test_wrong_token():
        response = client.get("/api/auth/users/me", headers={"Authorization": "Bearer wrong"})
        assert response.status_code == 401
        assert response.json() == {"detail": "Could not validate credentials"}

    def test_users_me_no_auth():
        response = client.get("/api/auth/users/me")
        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}

    def test_register_user_for_next_test():
        response = client.post("/api/auth/register", data={"username": "pytest", "password": "pytest"})
        assert response.status_code == 200
