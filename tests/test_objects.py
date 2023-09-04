from http import HTTPStatus

import pytest

from api.api_client import ApiClient
from api.objects_api import get_objects
from assertions.assertion_base import assert_status_code, assert_left_in_right_json, assert_response_body


class TestObjects:

    @pytest.fixture(scope='class')
    def client(self):
        return ApiClient()

    def test_get_objects(self, client, request):
        response = get_objects(client)
        assert_status_code(response, HTTPStatus.OK)
        assert_response_body(request, response)
        pass
