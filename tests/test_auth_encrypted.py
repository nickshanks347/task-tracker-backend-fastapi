import os
import sys

from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import Config, app

Config.ENCRYPT_JSON = 1
Config.DATA_DIR = "tests/data_encrypted"


with TestClient(app) as client:

    def test_register_user(set_env_vars_encrypted):
        response = client.post(
            "/api/auth/register", data={"username": "pytest", "password": "pytest"}
        )
        assert response.status_code == 201
        id = response.json()["id"]
        assert response.json() == {"username": "pytest", "id": id, "disabled": False}

    def test_registrations_disabled(set_env_vars_encrypted):
        Config.ENABLE_REGISTRATIONS = False
        response = client.post(
            "/api/auth/register", data={"username": "pytest1", "password": "pytest"}
        )
        assert response.status_code == 400
        assert response.json() == {"detail": "Registrations are disabled"}
        Config.ENABLE_REGISTRATIONS = True

    def test_register_user_already_exists(set_env_vars_encrypted):
        response = client.post(
            "/api/auth/register", data={"username": "pytest", "password": "pytest"}
        )
        assert response.status_code == 400
        assert response.json() == {"detail": "Username already registered"}

    def test_login_user(set_env_vars_encrypted):
        response = client.post(
            "/api/auth/token", data={"username": "pytest", "password": "pytest"}
        )
        assert response.status_code == 200
        access_token = response.json()["access_token"]
        assert response.json() == {"access_token": access_token, "token_type": "bearer"}
        assert response.cookies.get("auth") == f'"Bearer {access_token}"'

    def test_login_user_wrong_password(set_env_vars_encrypted):
        response = client.post(
            "/api/auth/token", data={"username": "pytest", "password": "wrong"}
        )
        assert response.status_code == 401
        assert response.json() == {"detail": "Incorrect username or password"}

    def test_login_user_wrong_username(set_env_vars_encrypted):
        response = client.post(
            "/api/auth/token", data={"username": "wrong", "password": "pytest"}
        )
        assert response.status_code == 401
        assert response.json() == {"detail": "Incorrect username or password"}

    def test_login_user_disabled(set_env_vars_encrypted):
        response = client.post(
            "/api/auth/register",
            data={"username": "disabled", "password": "disabled"},
            params={"disabled": "true"},
        )
        response = client.post(
            "/api/auth/token", data={"username": "disabled", "password": "disabled"}
        )
        assert response.status_code == 401
        assert response.json() == {"detail": "User is disabled"}

    def test_current_user(set_env_vars_encrypted):
        response = client.post(
            "/api/auth/token", data={"username": "pytest", "password": "pytest"}
        )
        access_token = response.json()["access_token"]
        response = client.get(
            "/api/auth/users/me", headers={"Authorization": "Bearer " + access_token}
        )
        id = response.json()["id"]
        assert response.status_code == 200
        assert response.json() == {"username": "pytest", "id": id, "disabled": False}

    def test_current_user_id(set_env_vars_encrypted):
        response = client.post(
            "/api/auth/token", data={"username": "pytest", "password": "pytest"}
        )
        access_token = response.json()["access_token"]
        response = client.get(
            "/api/auth/users/me/id", headers={"Authorization": "Bearer " + access_token}
        )
        id = response.json()["id"]
        assert response.status_code == 200
        assert response.json() == {"id": id}

    def test_login_wrong_token(set_env_vars_encrypted):
        response = client.get(
            "/api/auth/users/me", headers={"Authorization": "Bearer " + "invalid"}
        )
        assert response.status_code == 401
        assert response.json() == {"detail": "Could not validate credentials"}
