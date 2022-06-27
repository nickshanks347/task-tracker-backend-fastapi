import os
import sys
from fastapi.testclient import TestClient
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app

with TestClient(app) as client:

    def test_read_all_todos_no_auth():
        response = client.get('/api/todo/')
        assert response.status_code == 401
        assert response.json() == {'detail': 'Not authenticated'}

    def login():
        response = client.post('/api/auth/token', data={
            'username': 'pytest', 
            'password': 'pytest'
        })
        return response.json()['access_token']

    def test_create_todo():
        access_token = login()
        response = client.post('/api/todo/', json={
            'title': 'test',
            'done': False,
            'colour': 'red'
        }, headers={'Authorization': f'Bearer {access_token}'})
        assert response.status_code == 201
        assert response.json() == {
            'title': 'test',
            'done': False,
            'colour': 'red',
            'id': response.json()['id'],
            'created_at': response.json()['created_at'],
            'updated_at': response.json()['updated_at']
            }
        global id
        id = response.json()['id']

    def test_update_todo():
        access_token = login()
        response = client.put(f'/api/todo/{id}', json={
            'title': 'test2',
            'done': True,
            'colour': 'blue'
        }, headers={'Authorization': f'Bearer {access_token}'})
        assert response.status_code == 200
        assert response.json() == {
            'title': 'test2',
            'done': True,
            'colour': 'blue',
            'id': id,
            'created_at': response.json()['created_at'],
            'updated_at': response.json()['updated_at']
            }

    def test_read_todo():
        access_token = login()
        response = client.post(f'/api/todo/{id}', headers={'Authorization': f'Bearer {access_token}'})
        assert response.status_code == 200
        assert response.json() == {
            'title': 'test2',
            'done': True,
            'colour': 'blue',
            'id': id,
            'created_at': response.json()['created_at'],
            'updated_at': response.json()['updated_at']
            }

    def test_read_all_todos():
        access_token = login()
        response = client.get('/api/todo/', headers={'Authorization': f'Bearer {access_token}'})
        assert response.status_code == 200
        assert response.json() == {id: {
            "id": id,
            "title": "test2",
            "done": True,
            "colour": "blue",
            "created_at": response.json()[id]['created_at'],
            "updated_at": response.json()[id]['updated_at']
            }}
        
    def test_delete_todo():
        access_token = login()
        response = client.delete(f'/api/todo/{id}', headers={'Authorization': f'Bearer {access_token}'})
        assert response.status_code == 200
        assert response.json() == {'message': 'Task deleted'}

    def test_read_todo_not_found():
        access_token = login()
        response = client.post(f'/api/todo/test', headers={'Authorization': f'Bearer {access_token}'})
        assert response.status_code == 404
        assert response.json() == {'detail': 'Task not found'}