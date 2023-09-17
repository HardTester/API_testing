from http import HTTPStatus

from api.objects_api import get_object
from assertions.assertion_base import assert_response_body, assert_status_code
from utilities.files_utils import read_json_test_data


def should_be_posted_success(request, client, response, exp_obj):
    assert_response_body(request, response, exp_obj)

    exp_obj['id'] = response.json()['id']
    response = get_object(client, exp_obj['id'])
    assert_status_code(response, HTTPStatus.OK)
    assert exp_obj == response.json()


def should_be_update_success(request, client, response, exp_obj):
    assert_response_body(request, response, exp_obj, rmv_ids=False)

    response = get_object(client, exp_obj['id'])
    assert_status_code(response, HTTPStatus.OK)
    assert exp_obj == response.json()


def should_be_delete_success(request, response, obj_id):
    exp = read_json_test_data(request)
    exp['message'] = exp['message'].format(obj_id)
    assert_response_body(request, response, exp_obj=exp, rmv_ids=False)


def should_be_not_exist_delete_obj(request, response, obj_id):
    exp = read_json_test_data(request)
    exp['error'] = exp['error'].format(obj_id)
    assert_response_body(request, response, exp_obj=exp, rmv_ids=False)
