import pytest

from api.api_client import ApiClient


class TestObjects:

    @pytest.fixture(scope='class')
    def client(self):
        return ApiClient()

    def test_get_objects(self, client):
        pass