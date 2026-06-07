from fastapi import status
from fastapi.testclient import TestClient


def test_returns_200_with_health_details(client: TestClient):
    response = client.get('/health')
    health = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert health['message'] == 'ok'
    assert health['healthy']
