import json
import os


def get_project_path():
    separated = os.getcwd().rpartition('API_testing')
    return separated[0] + separated[1]


def get_test_data_path():
    return get_project_path() + "/test_data"


def get_common_response_path():
    return get_test_data_path() + "/common/responses"


def get_common_requests_path():
    return get_test_data_path() + "/common/requests"


def read_json_file_data(path):
    """
    возвращает содержимое json файла в виде dict
    :param path: путь до файла без расширения json
    """
    with open(f"{path}.json", "r") as f:
        data = json.load(f)
    return data


def read_json_test_data(request):
    """
    считывает данные для теста в формате json
    :param request: стандартный объект request фреймворка pytest
    :return: содержимое данных для теста из папки test_data
    """
    return read_json_file_data(f"{get_test_data_path()}/{request.node.originalname}")


def read_json_common_response_data(file_name):
    """
    считывает данные для теста в формате json из общей папки
    :param file_name: имя файла без расширения json
    :return: содержимое данных для теста из папки test_data/common/responses
    """
    return read_json_file_data(f"{get_common_response_path()}/{file_name}")


def read_json_common_request_data(file_name):
    """
    считывает данные для теста в формате json из общей папки
    :param file_name: имя файла без расширения json
    :return: содержимое данных для теста из папки test_data/common/requests
    """
    return read_json_file_data(f"{get_common_requests_path()}/{file_name}")
