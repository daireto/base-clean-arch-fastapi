from fastapi import status
from fastapi.testclient import TestClient

from src.main import app


def test_read_health():
    with TestClient(app) as client:
        response = client.get('/health')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'detail': 'ok'}
