import os

from httpx import Client, Response

from utilities.logger_utils import logger


class ApiClient(Client):
    def __init__(self):
        super().__init__(base_url=f"https://{os.getenv('RESOURSE_URL')}")

    def request(self, method, url, **kwargs) -> Response:
        """
        Расширение логики метода httpx request.
        Метод отправляет запрос на сервер, предварительно логируя тип запроса и его url.
        Логировать или нет задается в файле .env
        :param method: метод, который мы используем (POST, GET и.т.д)
        :param url: адрес, по которому отправляем запрос
        """

        if eval(os.getenv("USE_LOGS")):
            logger.info(f'{method} {url}')
        return super().request(method, url, **kwargs)
