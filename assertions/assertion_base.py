from typing import Type

from pydantic import BaseModel

from utilities.files_utils import read_json_test_data, read_json_common_response_data
from utilities.json_utils import compare_json_left_in_right, remove_ids


class LogMsg:
    """
    Базовый класс для построение логов AssertionError. Конструирует сообщение в свое поле _msg.
    """

    def __init__(self, where, response):
        self._msg = ""
        self._response = response
        self._where = where

    def add_request_url(self):
        """
        добавляет данные об отправленном на сервер запросе
        """
        self._msg += f"Содержимое отправляемого запроса (url, query params, тело):\n" \
                     f"\tURL: {self._response.request.url}\n"
        self._msg += f"\tmethod: {self._response.request.method}\n"
        self._msg += f"\theaders: {dict(self._response.request.headers)}\n"
        if hasattr(self._response.request, 'params') and self._response.request.params:
            self._msg += f"\tquery params: {self._response.request.params}\n"
        else:
            self._msg += f"\tquery params:\n"
        if hasattr(self._response.request, 'content') and self._response.request.read():
            self._msg += f"\tbody: {self._response.request.read()}\n"
        else:
            self._msg += f"\tbody:\n"
        return self

    def add_response_info(self):
        """
        добавляет информацию о содержимом тела ответа
        """
        self._msg += f"Тело ответа:\n\t{self._response.content}\n"
        return self

    def add_error_info(self, text):
        if text:
            self._msg += f"\n{text}\n"
        else:
            self._msg += "\n"
        return self

    def get_message(self):
        return self._msg


class BodyLogMsg(LogMsg):
    """
    Добавляет в логи результаты проверок тела ответа.
    """

    def __init__(self, response):
        super().__init__('В ТЕЛЕ ОТВЕТА', response)

    def add_compare_result(self, diff):
        """
        добавляет информацию о результате сравнения полученного json с эталоном
        :param diff: словарь с данными полей, которые после сравнения имеют разные значения
        """
        self._msg += f"{self._where} в json следующие поля не совпали с эталоном:\n"
        for key, value in diff.items():
            self._msg += f"ключ: {value['path']}\n\t\texpected: {value['expected']} \n\t\tactual: {value['actual']}\n"
        return self


class CodeLogMsg(LogMsg):
    """
    Добавляет в логи результаты проверки кода ответа.
    """

    def __init__(self, response):
        super().__init__('В КОДЕ ОТВЕТА', response)

    def add_compare_result(self, exp, act):
        """
        добавляет информацию об ожидаемом и полученной коде
        :param exp: ожидаемый код
        :param act: полученный код
        """
        self._msg += f"{self._where} \n\tожидался код: {exp}\n\tполученный код: {act}\n"
        return self


class BodyValueLogMsg(LogMsg):
    def __init__(self, response):
        super().__init__('В ТЕЛЕ ОТВЕТА', response)

    def add_compare_result(self, exp, act):
        """
        добавляет информацию о сравнении значений в теле ответа
        :param exp: ожидаемое значение
        :param act: полученное значение
        """
        self._msg += f"\texptected: {exp}\n\tactual: {act}\n"
        return self


def assert_status_code(response, expected_code):
    """
    сравнивает код ответа от сервера с ожидаемым
    :param response: полученный от сервера ответ
    :param expected_code: ожидаемый код ответа
    :raises AssertionError: если значения не совпали
    """
    assert expected_code == response.status_code, CodeLogMsg(response) \
        .add_compare_result(expected_code, response.status_code) \
        .add_request_url() \
        .add_response_info() \
        .get_message()


def assert_schema(response, model: Type[BaseModel]):
    """
    проверяет тело ответа на соответствие его схеме механизмами pydantic
    :param response: ответ от сервера
    :param model: модель, по которой будет проверяться схема json
    :raises ValidationError: если тело ответа не соответствует схеме
    """
    body = response.json()
    if isinstance(body, list):
        for item in body:
            model.model_validate(item, strict=True)
    else:
        model.model_validate(body, strict=True)


def assert_left_in_right_json(response, exp_json, actual_json):
    """
    проверяет, что все значения полей exp_json равны значениям полей в actual_json
    :param response: полученный ответ от сервера
    :param exp_json: ожидаемый эталонный json
    :param actual_json: полученый json
    :raises AssertionError: если в exp_json есть поля со значениями, которые отличаются или которых нет в actual_json
    """
    root = 'root:' if isinstance(actual_json, list) else ''
    compare_res = compare_json_left_in_right(exp_json, actual_json, key=root, path=root)
    assert not compare_res, BodyLogMsg(response) \
        .add_compare_result(compare_res) \
        .add_request_url() \
        .add_response_info() \
        .get_message()


def assert_response_body_fields(request, response, exp_obj=None, rmv_ids=True):
    """
    проверяет ответ от сервера, сравнивая ожидаемый объект с полученным
    :param request: стандартный объект request фреймворка pytest
    :param response: ответ от сервера
    :param exp_obj: ожидаемый объект
    :param rmv_ids: флаг: значение True - удаляет id из тела ответа при проверке, False - не удаляет
    """
    exp_json = read_json_test_data(request) if exp_obj is None else exp_obj
    act_json = remove_ids(response.json()) if rmv_ids else response.json()
    assert_left_in_right_json(response, exp_json, act_json)


def assert_response_body_value(response, exp, act, text=None):
    """
    проверяет ответ от сервера, сравнивая полученное значение с ожидаемым для тела запроса
    :param response: ответ от сервера
    :param exp: ожидаемое значение
    :param act: полученное значение
    :param text: дополнительный текст, который необходимо вывести при несовпадении exp и act
    """
    assert exp == act, BodyValueLogMsg(response) \
        .add_error_info(text) \
        .add_compare_result(exp, act) \
        .add_request_url() \
        .add_response_info() \
        .get_message()


def assert_empty_list(response):
    """
    проверяет, что тело ответа содержит пустой список
    :param response: ответ от сервера
    """
    assert_left_in_right_json(response, [], response.json())


def assert_bad_request(request, response):
    """
    проверяет, что тело ответа содержит данные BAD REQUEST
    :param request: стандартный объект request фреймворка pytest
    :param response: ответ от сервера
    """
    assert_response_body_fields(request, response, exp_obj=read_json_common_response_data("bad_request_response"))


def assert_not_found(request, response, obj_id):
    """
    проверяет, что тело ответа содержит данные NOT FOUND
    :param request: стандартный объект request фреймворка pytest
    :param response: ответ от сервера
    :param obj_id: id объекта, который сервер не нашел
    """
    exp = read_json_common_response_data("not_found_obj_response")
    exp['error'] = exp['error'].format(obj_id)
    assert_response_body_fields(request, response, exp_obj=exp)


def assert_not_exist(request, response, obj_id):
    """
    проверяет, что тело ответа содержит данные NOT EXIST
    :param request: стандартный объект request фреймворка pytest
    :param response: ответ от сервера
    :param obj_id: id объекта, который сервер не нашел
    """
    exp = read_json_test_data(request)
    exp['error'] = exp['error'].format(obj_id)
    assert_response_body_fields(request, response, exp_obj=exp, rmv_ids=False)
