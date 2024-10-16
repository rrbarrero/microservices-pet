import requests
import pytest


@pytest.fixture(scope="class")
def site_url():
    return "http://gateway:8000/api/v1/tasks"


class TestE2E:

    @classmethod
    def setup_class(cls):
        cls.client = requests.Session()
    
    def test_get(self, site_url):
        response = self.client.get(site_url)

        assert response.status_code == 200

    def test_post(self, site_url):
        task_data = {
                "title": "Test Task",
                "description": "This is a test task",
                "completed": "false",
            }
        response = self.client.post(site_url, json=task_data)
        
        assert response.status_code == 201
        