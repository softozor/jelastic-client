import logging

from .control_client import ControlClient
from .core import ApiClient
from .jps_client import JpsClient


class JelasticClientFactory:
    def __init__(self, api_url: str, api_token: str):
        self.api_client = ApiClient(api_url, api_token)
        self.logger = logging.getLogger(self.__class__.__name__)

    def create_jps_client(self) -> "JpsClient":
        self.logger.debug("creating JpsClient")
        return JpsClient(self.api_client)

    def create_control_client(self) -> "ControlClient":
        self.logger.debug("creating ControlClient")
        return ControlClient(self.api_client)
