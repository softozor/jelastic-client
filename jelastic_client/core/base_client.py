from abc import ABC, abstractmethod
from typing import Dict

from . import ApiClient


def success_response(response: Dict) -> bool:
    return response["result"] == 0


class BaseClient(ABC):

    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    @property
    @abstractmethod
    def grp_cls(self):
        raise NotImplementedError

    def execute(self, fnc: str, **kwargs) -> Dict:
        response = self.api_client.execute(
            self._fnc(fnc),
            **kwargs
        )
        return response

    def _fnc(self, fnc_name: str):
        return f"{self.grp_cls}.{fnc_name}"
