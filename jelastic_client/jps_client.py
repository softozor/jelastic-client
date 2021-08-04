import logging
from typing import Dict

from .core import ApiClient


class JpsClient:

    def __init__(self, api_client: ApiClient):
        self.api_client = api_client
        self.logger = logging.getLogger(self.__class__.__name__)
        self.grp_cls = "marketplace.jps"

    def install(self, filename: str, env_name: str) -> Dict:
        with open(filename) as file:
            manifest_content = file.read()

            response = self.api_client.execute(
                self._fnc("install"),
                jps=manifest_content,
                envName=env_name
            )

            return response

    # TODO: this should be part of an abstract JelasticClient
    def _fnc(self, fnc_name: str):
        return f"{self.grp_cls}.{fnc_name}"
