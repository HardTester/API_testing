from http import HTTPStatus

import pytest

from api.api_client import ApiClient
from api.objects_api import get_objects, get_object, post_object, put_object, delete_object
from assertions.assertion_base import assert_status_code, assert_response_body, assert_bad_request, \
    assert_not_exist, assert_empty_list, assert_schema
from assertions.objects_assertion import should_be_posted_success, should_be_update_success, should_be_delete_success, \
    should_be_not_exist_delete_obj, should_be_valid_objects_response
from models.object_models import ObjectOutSchema, ObjectCreateOutSchema, CustomObjCreateOutSchema, \
    ObjectUpdateOutSchema, CustomObjUpdateOutSchema
from utilities.files_utils import read_json_test_data, read_json_common_request_data


class TestObjects:

    @pytest.fixture(scope='class')
    def client(self):
        return ApiClient()

    def test_get_objects(self, client, request):
        response = get_objects(client)
        assert_status_code(response, HTTPStatus.OK)
        assert_response_body(request, response)

    @pytest.mark.parametrize("param", [{"index": 0, "ids": [1]}, {"index": 1, "ids": [1, 2]}])
    def test_get_objects_id_param(self, client, request, param):
        response = get_objects(client, *param['ids'])
        assert_status_code(response, HTTPStatus.OK)
        should_be_valid_objects_response(request, response, param)

    def test_get_objects_not_exist_id(self, client):
        response = get_objects(client, 8523697415)
        assert_status_code(response, HTTPStatus.OK)
        assert_empty_list(response)

    def test_get_objects_invalid_id(self, client):
        response = get_objects(client, "kjdsf23321")
        assert_status_code(response, HTTPStatus.OK)
        assert_empty_list(response)

    def test_get_object(self, client, request):
        response = get_object(client, 7)
        assert_status_code(response, HTTPStatus.OK)
        assert_schema(response, ObjectOutSchema)
        assert_response_body(request, response)

    def test_get_object_not_exist(self, client, request):
        response = get_object(client, "ff8081818a394cb8018a790e1d534578")
        assert_status_code(response, HTTPStatus.NOT_FOUND)
        assert_response_body(request, response)

    def test_post_object_empty_body(self, client, request):
        response = post_object(client, json={})

        assert_status_code(response, HTTPStatus.OK)
        assert_schema(response, ObjectCreateOutSchema)
        exp_obj = {"data": None, "name": None}
        should_be_posted_success(request, client, response, exp_obj)

    def test_post_object_with_full_body(self, client, request):
        exp_obj = read_json_common_request_data("valid_post_object")
        response = post_object(client, json=exp_obj)

        assert_status_code(response, HTTPStatus.OK)
        assert_schema(response, CustomObjCreateOutSchema)
        should_be_posted_success(request, client, response, exp_obj)

    def test_post_object_send_invalid_json(self, client, request):
        response = post_object(client, content='{"name",}', headers={"Content-Type": "application/json"})

        assert_status_code(response, HTTPStatus.BAD_REQUEST)
        assert_bad_request(request, response)

    def test_put_object_with_empty_body(self, client, request):
        post_obj = read_json_common_request_data("valid_post_object")
        response = post_object(client, json=post_obj)
        assert_status_code(response, HTTPStatus.OK)

        exp_json = {"id": response.json()['id'], "name": None, "data": None}
        response = put_object(client, exp_json['id'], json={})
        assert_status_code(response, HTTPStatus.OK)
        assert_schema(response, ObjectUpdateOutSchema)
        should_be_update_success(request, client, response, exp_json)

    def test_put_object_with_full_body(self, client, request):
        post_obj = read_json_common_request_data("valid_post_object")
        response = post_object(client, json=post_obj)
        assert_status_code(response, HTTPStatus.OK)

        put_obj = read_json_test_data(request)
        put_obj_id = response.json()['id']
        response = put_object(client, put_obj_id, json=put_obj)
        assert_status_code(response, HTTPStatus.OK)
        assert_schema(response, CustomObjUpdateOutSchema)

        put_obj['id'] = put_obj_id
        should_be_update_success(request, client, response, put_obj)

    def test_put_object_send_invalid_json(self, client, request):
        response = post_object(client, json=read_json_common_request_data("valid_post_object"))
        assert_status_code(response, HTTPStatus.OK)

        response = put_object(client, response.json()['id'], content='{"name",}',
                              headers={"Content-Type": "application/json"})
        assert_status_code(response, HTTPStatus.BAD_REQUEST)
        assert_bad_request(request, response)

    def test_put_object_update_non_exist_obj(self, client, request):
        response = post_object(client, json=read_json_common_request_data("valid_post_object"))
        assert_status_code(response, HTTPStatus.OK)

        obj_id = "ff8081818a194cb8018a79e7545545ac"
        response = put_object(client, obj_id, json={})
        assert_status_code(response, HTTPStatus.NOT_FOUND)
        assert_not_exist(request, response, obj_id)

    def test_delete_exist_object(self, client, request):
        response = post_object(client, json=read_json_common_request_data("valid_post_object"))
        assert_status_code(response, HTTPStatus.OK)

        obj_id = response.json()['id']
        response = delete_object(client, obj_id)
        assert_status_code(response, HTTPStatus.OK)
        should_be_delete_success(request, response, obj_id)

    def test_delete_not_exist_object(self, client, request):
        response = post_object(client, json=read_json_common_request_data("valid_post_object"))
        assert_status_code(response, HTTPStatus.OK)

        obj_id = "ff8081818a194cb8018a79e7545545ac"
        response = delete_object(client, obj_id)
        assert_status_code(response, HTTPStatus.NOT_FOUND)
        should_be_not_exist_delete_obj(request, response, obj_id)
