from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_create_resource_and_return_201():
    response = client.post('/resources/', data={'url': 'https://example.com'})

    assert response.status_code == 201
    assert response.json() == {'url': 'https://example.com'}
