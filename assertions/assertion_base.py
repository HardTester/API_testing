from typing import Type

from pydantic import BaseModel

from utilities.json_utils import compare_json_left_in_right


class LogMsg:
    """
    Базовый класс для построение логов AssertionError. Конструирует сообщение в свое поле _msg.
    """

    def __init__(self, where, response):
        self._msg = ""
        self.response = response
        self.where = where

    def add_user_info(self):
        self._msg += f"ФАКТИЧЕСКИЕ ЗНАЧЕНИЕ НЕ СОВПАЛО С ОЖИДАЕМЫМ\n" \
                     f"Имя пользователя:\n\t{self.response.client.get_login()}\n"
        return self

    def add_request_url(self):
        """
        Добавляет данные об отправленном на сервер запросе.
        """
        self._msg += f"Содержимое отправляемого запроса (url, query params, тело):\n" \
                     f"\tURL: {self.response.request.url}\n"
        self._msg += f"\tmethod: {self.response.request.method}\n"
        self._msg += f"\theaders: {dict(self.response.request.headers)}\n"
        if hasattr(self.response.request, 'params') and self.response.request.params:
            self._msg += f"\tquery params: {self.response.request.params}\n"
        else:
            self._msg += f"\tquery params:\n"
        if hasattr(self.response.request, 'content') and self.response.request.read():
            self._msg += f"\tbody: {self.response.request.read()}\n"
        else:
            self._msg += f"\tbody:\n"
        return self

    def add_response_info(self):
        self._msg += f"Тело ответа:\n\t{self.response.content}\n"
        return self

    def get_message(self):
        return self._msg


class BodyLogMsg(LogMsg):
    """
    Добавляет в логи результаты проверок тела ответа
    """

    def __init__(self, response):
        super().__init__('В ТЕЛЕ ОТВЕТА', response)

    def add_compare_result(self, diff):
        """
        Добавляет информацию о результате сравнения полученного json с эталоном.
        """
        self._msg += f"{self.where} в json следующие поля не совпали с эталоном:\n"
        for key, value1, value2 in diff:
            if value1 == 'none':
                value1 = ''
            elif isinstance(value1, str):
                value1 = f"'{value1}'"
            if value2 == 'none':
                value2 = ''
            elif isinstance(value2, str):
                value2 = f"'{value2}'"
            if isinstance(value1, list) and isinstance(value2, list):
                self._msg += f"{key}\n\texpected (count={len(value1)}) " \
                             f":{value1}\n\tactual (count={len(value2)}):{value2}\n"
            else:
                self._msg += f"{key}\n\texpected:{value1}\n\tactual:{value2}\n"
        return self

    def add_expected_info(self, exp):
        self._msg += f"Проверяемые поля ответа:\n\t{exp}\n"
        return self

    def add_compare_values(self, exp, act):
        """
        Добавляет информацию о результате сравнения тела ответа с эталоном,
        когда в теле ответа только единичное значение (без json).
        """
        exp = f"'{exp}'" if isinstance(exp, str) else exp
        act = f"'{act}'" if isinstance(act, str) else act
        self._msg += f"{self.where} ожидаемое значение не совпало с фактическим\n" \
                     f"\texpected: {exp}\n" \
                     f"\tactual: {act}\n"
        return self


class CodeLogMsg(LogMsg):
    """
    Добавляет в логи результаты проверки кода ответа
    """

    def __init__(self, response):
        super().__init__('В КОДЕ ОТВЕТА', response)

    def add_compare_result(self, exp, act):
        self._msg += f"{self.where} \n\tожидался код: {exp}\n\tполученный код: {act}\n"
        return self


def assert_status_code(response, expected):
    """
    Сравнивает код ответа с ожидаемым.
    :param response: полученный от сервера ответ
    :param expected: ожидаемый код ответа.
    :raises AssertionError: если значения не совпали
    """
    assert expected == response.status_code, CodeLogMsg(response) \
        .add_user_info() \
        .add_request_url() \
        .add_compare_result(expected, response.status_code) \
        .add_response_info() \
        .get_message()


def assert_schema(response, model: Type[BaseModel]):
    """
    Проверяет json на соответствие его схеме механизмами pydantic.
    :param response: ответ от сервера
    :param model: модель, по которой будет проверяться схема json
    :raises ValidationError: если json не соответствует схеме
    """
    body = response.json()
    if isinstance(body, list):
        for item in body:
            model.model_validate(item, strict=True)
    else:
        model.model_validate(body, strict=True)


def assert_left_in_right_json(response, exp_json, actual_json):
    """
    Убеждается, что все значения полей exp_json равны значениям полей в actual_json.
    :param response: полученный ответ от сервера
    :param exp_json: ожидаемый эталонный json
    :param actual_json: полученый json
    :raises AssertionError: если в exp_json есть поля, значение которых отличается от эталона
    """
    compare_res = compare_json_left_in_right(exp_json, actual_json)
    assert not compare_res, BodyLogMsg(response) \
        .add_user_info() \
        .add_request_url() \
        .add_compare_result(compare_res) \
        .add_expected_info(exp_json) \
        .add_response_info() \
        .get_message()
