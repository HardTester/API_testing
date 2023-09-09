from http import HTTPStatus

import pytest

from api.api_client import ApiClient
from api.objects_api import get_objects, get_object, post_object
from assertions.assertion_base import assert_status_code, assert_response_body
from assertions.objects_assertion import should_be_valid_object
from utilities.files_utils import read_test_data


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

    def test_post_object_empty_body(self, client, request):
        response = post_object(client, obj={})

        assert_status_code(response, HTTPStatus.OK)
        should_be_valid_object(request, client, response)

    def test_post_object_empty_body(self, client, request):
        response = post_object(client, obj={})

        assert_status_code(response, HTTPStatus.OK)
        exp_obj = read_test_data(request)
        should_be_valid_object(request, client, response, exp_obj)

    def test_post_object_with_full_body(self, client, request):
        send_obj = read_test_data(request)
        response = post_object(client, obj=send_obj)

        assert_status_code(response, HTTPStatus.OK)
        should_be_valid_object(request, client, response, send_obj)
