from http import HTTPStatus

from api.objects_api import get_object
from assertions.assertion_base import assert_response_body, assert_status_code
from utilities.files_utils import read_test_data


def should_be_valid_object(request, client, response):
    exp_obj = read_test_data(request)
    assert_response_body(request, response, exp_obj)

    exp_obj['id'] = response.json()['id']
    response = get_object(client, exp_obj['id'])
    assert_status_code(response, HTTPStatus.OK)
    assert exp_obj == response.json()
