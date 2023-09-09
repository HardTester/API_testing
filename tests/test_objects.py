from http import HTTPStatus

import pytest

from api.api_client import ApiClient
from api.objects_api import get_objects, get_object
from assertions.assertion_base import assert_status_code, assert_left_in_right_json, assert_response_body


class TestObjects:

    @pytest.fixture(scope='class')
    def client(self):
        return ApiClient()

    def test_get_objects(self, client, request):
        response = get_objects(client)
        assert_status_code(response, HTTPStatus.OK)
        assert_response_body(request, response)

    def test_get_object(self, client, request):
        response = get_object(client, 7)
        assert_status_code(response, HTTPStatus.OK)
        assert_response_body(request, response)

    def test_get_object_not_exist(self, client, request):
        response = get_object(client, "ff8081818a394cb8018a790e1d534578")
        assert_status_code(response, HTTPStatus.NOT_FOUND)
        assert_response_body(request, response)
