from typing import Optional

from jelastic_client.core import ApiClient, BaseClient, who_am_i


class FileClient(BaseClient):
    jelastic_group = "environment"

    jelastic_class = "file"

    def __init__(self, api_client: ApiClient):
        super().__init__(api_client)

    def read(
        self,
        env_name: str,
        path: str,
        node_type: Optional[str] = None,
        node_group: Optional[str] = None,
        node_id: Optional[str] = None,
    ) -> str:
        response = self._execute(
            who_am_i(),
            envName=env_name,
            path=path,
            nodeType=node_type,
            nodeGroup=node_group,
            nodeid=node_id,
        )
        return response["body"]
