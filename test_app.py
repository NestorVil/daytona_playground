import pytest
import app
from flask import json

@pytest.fixture
def client():
    app.app.config['TESTING'] = True
    with app.app.test_client() as client:
        # Reset the todos and current_id before each test
        app.todos.clear()
        app.current_id = 1
        yield client

def test_create_todo(client):
    response = client.post('/todos', json={'task': 'Test task'})
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['task'] == 'Test task'
    assert data['completed'] is False
    assert 'id' in data


def test_create_todo_missing_task(client):
    response = client.post('/todos', json={})
    assert response.status_code == 400


def test_list_todos(client):
    client.post('/todos', json={'task': 'Task 1'})
    client.post('/todos', json={'task': 'Task 2'})
    response = client.get('/todos')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2


def test_update_todo(client):
    client.post('/todos', json={'task': 'Old task'})
    response = client.put('/todos/1', json={'task': 'Updated task'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['task'] == 'Updated task'


def test_update_todo_missing_task(client):
    client.post('/todos', json={'task': 'Old task'})
    response = client.put('/todos/1', json={})
    assert response.status_code == 400


def test_update_todo_not_found(client):
    response = client.put('/todos/99', json={'task': 'Updated task'})
    assert response.status_code == 404


def test_delete_todo(client):
    client.post('/todos', json={'task': 'To be deleted'})
    response = client.delete('/todos/1')
    assert response.status_code == 204
    # Confirm deletion
    response = client.get('/todos')
    data = json.loads(response.data)
    assert len(data) == 0


def test_delete_todo_not_found(client):
    response = client.delete('/todos/99')
    assert response.status_code == 404


def test_mark_complete(client):
    client.post('/todos', json={'task': 'Task to complete'})
    response = client.post('/todos/1/complete')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['completed'] is True


def test_mark_complete_not_found(client):
    response = client.post('/todos/99/complete')
    assert response.status_code == 404

