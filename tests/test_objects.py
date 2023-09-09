from http import HTTPStatus

import pytest

from api.api_client import ApiClient
from api.objects_api import get_objects, get_object, post_object, put_object
from assertions.assertion_base import assert_status_code, assert_response_body, assert_bad_request, \
    assert_not_exist_response
from assertions.objects_assertion import should_be_valid_post_object, should_be_valid_update_object
from utilities.files_utils import read_json_test_data


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
        response = post_object(client, json={})

        assert_status_code(response, HTTPStatus.OK)
        exp_obj = read_json_test_data(request)
        should_be_valid_post_object(request, client, response, exp_obj)

    def test_post_object_with_full_body(self, client, request):
        send_obj = read_json_test_data(request)
        response = post_object(client, json=send_obj)

        assert_status_code(response, HTTPStatus.OK)
        should_be_valid_post_object(request, client, response, send_obj)

    def test_post_object_send_invalid_json(self, client, request):
        response = post_object(client, content='{"name",}', headers={"Content-Type": "application/json"})

        assert_status_code(response, HTTPStatus.BAD_REQUEST)
        assert_response_body(request, response)

    def test_put_object_with_empty_body(self, client, request):
        send_objects = read_json_test_data(request)
        response = post_object(client, json=send_objects['post'])
        assert_status_code(response, HTTPStatus.OK)

        save_obj = {"id": response.json()['id'], "name": None, "data": None, **send_objects['put']}
        response = put_object(client, save_obj['id'], json=send_objects['put'])
        assert_status_code(response, HTTPStatus.OK)
        should_be_valid_update_object(request, client, response, save_obj)

    def test_put_object_with_full_body(self, client, request):
        send_objects = read_json_test_data(request)
        response = post_object(client, json=send_objects['post'])
        assert_status_code(response, HTTPStatus.OK)

        save_obj = {"id": response.json()['id'], **send_objects['put']}
        response = put_object(client, save_obj['id'], json=send_objects['put'])
        assert_status_code(response, HTTPStatus.OK)
        should_be_valid_update_object(request, client, response, save_obj)

    def test_put_object_send_invalid_json(self, client, request):
        response = post_object(client, json=read_json_test_data(request))
        assert_status_code(response, HTTPStatus.OK)

        response = put_object(client, response.json()['id'], content='{"name",}',
                              headers={"Content-Type": "application/json"})
        assert_status_code(response, HTTPStatus.BAD_REQUEST)
        assert_bad_request(request, response)

    def test_put_object_update_non_exist_obj(self, client, request):
        response = post_object(client, json=read_json_test_data(request))
        assert_status_code(response, HTTPStatus.OK)

        obj_id = "ff8081818a194cb8018a79e7545545ac"
        response = put_object(client, obj_id, json={})
        assert_status_code(response, HTTPStatus.NOT_FOUND)
        assert_not_exist_response(request, response, obj_id)
