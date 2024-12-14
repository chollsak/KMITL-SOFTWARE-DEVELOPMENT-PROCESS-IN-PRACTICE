import pytest 
from app.routes import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_list_users(client):
    response = client.get('/user/')
    assert response.status_code == 200
    assert response.json == {}

def test_create_user(client):
    response = client.post('/user/new', json={"username": "test_user", "minlen": 5})
    assert response.status_code == 201
    assert "id" in response.json

def test_create_user_invalid(client):
    response = client.post('/user/new', json={"username": "1invalid_user", "minlen": 5})
    assert response.status_code == 400
    assert "error" in response.json

def test_update_user(client):
    # Create a user first
    response = client.post('/user/new', json={"username": "test_user", "minlen": 5})
    user_id = response.json['id']

    # Update the user
    response = client.put(f'/user/{user_id}', json={"username": "updated_user", "minlen": 5})
    assert response.status_code == 200
    assert response.json["message"] == "User updated successfully"

def test_update_user_not_found(client):
    response = client.put('/user/999', json={"username": "updated_user", "minlen": 5})
    assert response.status_code == 404
    assert "error" in response.json

def test_get_user(client):
    # Create a user first
    response = client.post('/user/new', json={"username": "test_user", "minlen": 5})
    user_id = response.json['id']

    # Retrieve the user
    response = client.get(f'/user/{user_id}')
    assert response.status_code == 200
    assert response.json["username"] == "test_user"

def test_get_user_not_found(client):
    response = client.get('/user/999')
    assert response.status_code == 404
    assert "error" in response.json

def test_delete_user(client):
    # Create a user first
    response = client.post('/user/new', json={"username": "test_user", "minlen": 5})
    user_id = response.json['id']

    # Delete the user
    response = client.delete(f'/user/{user_id}')
    assert response.status_code == 200
    assert response.json["message"] == "User deleted successfully"

def test_delete_user_not_found(client):
    response = client.delete('/user/999')
    assert response.status_code == 404
    assert "error" in response.json
