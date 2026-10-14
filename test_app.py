import pytest
import json
from app import app, todos

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_todo(client):
    response = client.post('/todos', json={'task': 'Test task'})
    assert response.status_code == 201
    data = response.get_json()
    assert data['task'] == 'Test task'
    assert data['completed'] is False

def test_create_todo_no_task(client):
    response = client.post('/todos', json={})
    assert response.status_code == 400

def test_list_todos(client):
    # Clear todos
    todos.clear()
    # Seed with two todos
    client.post('/todos', json={'task': 'Task 1'})
    client.post('/todos', json={'task': 'Task 2'})
    response = client.get('/todos')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2

def test_update_todo(client):
    todos.clear()
    res = client.post('/todos', json={'task': 'Initial task'})
    todo_id = res.get_json()['id']
    response = client.put(f'/todos/{todo_id}', json={'task': 'Updated task'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['task'] == 'Updated task'

def test_update_todo_not_found(client):
    response = client.put('/todos/9999', json={'task': 'Updated task'})
    assert response.status_code == 404

def test_delete_todo(client):
    todos.clear()
    res = client.post('/todos', json={'task': 'Task to delete'})
    todo_id = res.get_json()['id']
    response = client.delete(f'/todos/{todo_id}')
    assert response.status_code == 204

def test_delete_todo_not_found(client):
    response = client.delete('/todos/9999')
    assert response.status_code == 404

def test_mark_complete(client):
    todos.clear()
    res = client.post('/todos', json={'task': 'Incomplete task'})
    todo_id = res.get_json()['id']
    response = client.post(f'/todos/{todo_id}/complete')
    assert response.status_code == 200
    data = response.get_json()
    assert data['completed'] is True

def test_mark_complete_not_found(client):
    response = client.post('/todos/9999/complete')
    assert response.status_code == 404
