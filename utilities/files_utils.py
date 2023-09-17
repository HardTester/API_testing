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
    """
    with open(f"{path}.json", "r") as f:
        data = json.load(f)
    return data


def read_json_test_data(request):
    return read_json_file_data(f"{get_test_data_path()}/{request.node.originalname}")


def read_json_common_response_data(file_name):
    return read_json_file_data(f"{get_common_response_path()}/{file_name}")


def read_json_common_request_data(file_name):
    return read_json_file_data(f"{get_common_requests_path()}/{file_name}")
