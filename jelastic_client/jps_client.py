from .core import ApiClient


class JpsClient:

    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    def install(self) -> None:
        print('install')
