from fastapi import status
from fastapi.testclient import TestClient

from src.main import app


class TestCreateResource:
    def test_create_resource_and_return_200(self):
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

    def test_raise_when_resource_url_is_invalid_and_return_400(self):
        data = {
            'name': 'Random Image',
            'url': 'not-a-valid-url',
            'type': 'image',
        }

        with TestClient(app) as client:
            response = client.post('/resources/', json=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_raise_when_resource_type_is_not_supported_and_return_400(self):
        data = {
            'name': 'Random Image',
            'url': 'https://example.com',
            'type': 'not-a-valid-type',
        }

        with TestClient(app) as client:
            response = client.post('/resources/', json=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
