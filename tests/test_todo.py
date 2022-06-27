import os
import sys
from fastapi.testclient import TestClient
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app


def test_read_all_todos_no_auth():
    with TestClient(app) as client:
        response = client.get('/api/todo')
        assert response.status_code == 401
        assert response.json() == {'detail': 'Not authenticated'}

