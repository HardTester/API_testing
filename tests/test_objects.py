from http import HTTPStatus

import pytest

from api.api_client import ApiClient
from api.objects_api import get_objects
from assertions.assertion_base import assert_status_code


class TestObjects:

    @pytest.fixture(scope='class')
    def client(self):
        return ApiClient()

    def test_get_objects(self, client):
        response = get_objects(client)
        assert_status_code(response, HTTPStatus.OK)
        pass
