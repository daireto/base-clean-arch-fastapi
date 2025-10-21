from fastapi import status
from fastapi.testclient import TestClient

from main import app


def test_returns_200_and_health_details():
    # Act
    with TestClient(app) as client:
        response = client.get('/health')
    health = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert health['message'] == 'pong'
    assert health['status'] == 'ok'
