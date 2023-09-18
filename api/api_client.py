import os

from httpx import Client, Response

from utilities.logger_utils import logger


class ApiClient(Client):
    """
    Расширение стандартного клиента httpx.
    """

    def __init__(self):
        super().__init__(base_url=f"https://{os.getenv('RESOURSE_URL')}")

    def request(self, method, url, **kwargs) -> Response:
        """
        расширение логики метода httpx request с добавлением логирования типа запроса и его url,
        логировать или нет задается в файле .env
        :param method: метод, который мы используем (POST, GET и.т.д)
        :param url: путь на домене, по которому отправляем запрос
        """

        if eval(os.getenv("USE_LOGS")):
            logger.info(f'{method} {url}')
        return super().request(method, url, **kwargs)
