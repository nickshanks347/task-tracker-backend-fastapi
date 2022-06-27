import os
import sys
from fastapi.testclient import TestClient
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app

with TestClient(app) as client:

    def test_register_user():
        response = client.post('/api/auth/register', data={
            'username': 'pytest',
            'password': 'pytest'
        })
        assert response.status_code == 201
        id = response.json()['id']
        assert response.json() == {'username': 'pytest', "id": id, "disabled": False}

    def test_register_user_already_exists():
        response = client.post('/api/auth/register', data={
            'username': 'pytest',
            'password': 'pytest'
        })
        assert response.status_code == 400
        assert response.json() == {'detail': 'Username already registered'}

    def test_login_user():
        response = client.post('/api/auth/token', data={
            'username': 'pytest',
            'password': 'pytest'
        })
        assert response.status_code == 200
        access_token = response.json()['access_token']
        assert response.json() == {"access_token": access_token, "token_type": "bearer"}

    def test_login_user_wrong_password():
        response = client.post('/api/auth/token', data={
            'username': 'pytest',
            'password': 'wrong'
        })
        assert response.status_code == 401
        assert response.json() == {'detail': 'Incorrect username or password'}

    def test_login_user_wrong_username():
        response = client.post('/api/auth/token', data={
            'username': 'wrong',
            'password': 'pytest'
        })
        assert response.status_code == 401
        assert response.json() == {'detail': 'Incorrect username or password'}

    def test_current_user():
        response = client.post('/api/auth/token', data={
            'username': 'pytest',
            'password': 'pytest'
            })
        access_token = response.json()['access_token']
        response = client.get('/api/auth/users/me', headers={
            'Authorization': 'Bearer ' + access_token
        })
        id = response.json()['id']
        assert response.status_code == 200
        assert response.json() == {"username": "pytest", "id": id, "disabled": False}
        
    def test_current_user_id():
        response = client.post('/api/auth/token', data={
            'username': 'pytest',
            'password': 'pytest'
            })
        access_token = response.json()['access_token']
        response = client.get('/api/auth/users/me/id', headers={
            'Authorization': 'Bearer ' + access_token
        })
        id = response.json()['id']
        assert response.status_code == 200
        assert response.json() == {"id": id}

    def test_login_wrong_token():
        response = client.get('/api/auth/users/me', headers={
            'Authorization': 'Bearer ' + 'invalid'
        })
        assert response.status_code == 401
        assert response.json() == {'detail': 'Could not validate credentials'}