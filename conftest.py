import logging
import os

from dotenv import load_dotenv

from utilities.logger_utils import logger


def pytest_configure(config):
    # устанавливаем текущую директорию на корень проекта (это позволит прописывать относительные пути к файлам)
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # загружаем переменные-параметры из файла /.env
    load_dotenv(dotenv_path=".env")

    # задаем параметры логгера
    path = "logs/"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    file_handler = logging.FileHandler(path + "/info.log", "w")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter("%(lineno)d: %(asctime)s %(message)s"))

    # создаем кастомный логгер
    custom_logger = logging.getLogger("custom_loger")
    custom_logger.setLevel(logging.INFO)
    custom_logger.addHandler(file_handler)


def pytest_runtest_setup(item):
    logger.info(f"{item.name}:")
