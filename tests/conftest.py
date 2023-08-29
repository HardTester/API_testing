import logging

from dotenv import load_dotenv

from utilities.files_utils import get_project_path


def pytest_configure(config):
    load_dotenv(dotenv_path=get_project_path() + '/.env')

    # установка параметров логирования
    params = {
        "level": logging.INFO,
        "format": "%(lineno)d: %(asctime)s %(message)s",
        "filename": f"{get_project_path()}/logs/info.log", "filemode": "w"
    }
    logging.basicConfig(**params)
