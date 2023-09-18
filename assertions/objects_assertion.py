from http import HTTPStatus

from api.objects_api import get_object
from assertions.assertion_base import assert_response_body_fields, assert_status_code, assert_response_body_value
from utilities.files_utils import read_json_test_data


def should_be_valid_objects_response(request, response, param):
    # убеждаемся, что в ответе столько объектов, сколько мы ожидаем
    exp = read_json_test_data(request)[param['index']]
    exp_len, act_len = len(exp), len(response.json())
    assert_response_body_value(response, exp_len, act_len,
                               text="ОЖИДАЕМОЕ КОЛИЧЕСТВО ОБЪЕКТОВ НЕ СОВПАЛО С ФАКТИЧЕСКИМ")

    # убеждаемся в корректности значений полей полученных объектов
    assert_response_body_fields(request, response, exp)


def should_be_posted_success(request, client, response, exp_obj):
    # убеждаемся в корректности значений полей тела ответа
    assert_response_body_fields(request, response, exp_obj)

    # убеждаемся, что объект корректно сохранен на сервере
    exp_obj['id'] = response.json()['id']
    response = get_object(client, exp_obj['id'])
    assert_status_code(response, HTTPStatus.OK)
    assert exp_obj == response.json()


def should_be_updated_success(request, client, response, exp_obj):
    # убеждаемся в корректности значений полей тела ответа
    assert_response_body_fields(request, response, exp_obj, rmv_ids=False)

    # убеждаемся, что объект корректно обновлен на сервере
    response = get_object(client, exp_obj['id'])
    assert_status_code(response, HTTPStatus.OK)
    assert exp_obj == response.json()


def should_be_deleted_success(request, response, obj_id):
    exp = read_json_test_data(request)
    exp['message'] = exp['message'].format(obj_id)
    assert_response_body_fields(request, response, exp_obj=exp, rmv_ids=False)
