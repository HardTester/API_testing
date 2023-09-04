import json
import os


def get_project_path():
    separated = os.getcwd().rpartition('API_testing')
    return separated[0] + separated[1]


def get_test_data_path():
    return get_project_path() + "/test_data"


def read_json_file_data(path):
    """
    возвращает содержимое json файла
    """
    with open(f"{path}.json", "r") as f:
        data = json.load(f)
    return data
