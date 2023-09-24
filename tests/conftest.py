import logging

from dotenv import load_dotenv

from utilities.files_utils import get_project_path
from utilities.logger_utils import logger


def pytest_configure(config):
    # загружаем переменные-параметры из файла /.env
    load_dotenv(dotenv_path=get_project_path() + '/.env')

    # задаем паарметры логгера
    file_handler = logging.FileHandler(f"{get_project_path()}/logs/info.log", "w")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter("%(lineno)d: %(asctime)s %(message)s"))

    # создаем кастомный логгер
    custom_logger = logging.getLogger("custom_loger")
    custom_logger.setLevel(logging.INFO)
    custom_logger.addHandler(file_handler)


def pytest_runtest_setup(item):
    logger.info(f"{item.name}:")
