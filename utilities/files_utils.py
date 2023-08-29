import os


def get_project_path():
    separated = os.getcwd().rpartition('API_testing')
    return separated[0] + separated[1]
