import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_greet(client):
    # Test default greeting
    response = client.get('/api/greet')
    assert response.status_code == 200
    assert response.json == {"message": "Hello, World!"}

    # Test greeting with a name
    response = client.get('/api/greet?name=New')
    assert response.status_code == 200
    assert response.json == {"message": "Hello, New!"}