from fastapi import status
from fastapi.testclient import TestClient

from main import app


def test_create_resource_and_return_200():
    data = {
        'name': 'Random Image',
        'url': 'https://picsum.photos/200/200',
        'type': 'image',
    }

    with TestClient(app) as client:
        response = client.post('/resources/', json=data)

    assert response.status_code == status.HTTP_200_OK

    response_content = response.json()
    assert response_content['name'] == data['name']
    assert response_content['url'] == data['url']
    assert response_content['type'] == data['type']
