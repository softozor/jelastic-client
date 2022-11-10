import random
import string

import simplejson as json

from .core import (
    ApiClient,
    BaseClient,
    who_am_i,
    JelasticClientException
)
from .env_info import EnvInfo
from .env_settings import EnvSettings
from .env_status import EnvStatus
from .node_settings import MultipleNodeSettings


class ControlClient(BaseClient):
    jelastic_group = "environment"

    jelastic_class = "control"

    def __init__(self, api_client: ApiClient):
        super().__init__(api_client)

    def generate_random_env_name(self):
        env_name = self._create_random_env_name()
        while self.get_env_info(env_name).exists():
            env_name = self._create_random_env_name()
        return env_name

    def create_environment(self, env: EnvSettings, nodes: MultipleNodeSettings) -> EnvInfo:
        env_json = json.dumps(env)
        nodes_json = json.dumps(nodes)
        response = self._execute(who_am_i(), env=env_json, nodes=nodes_json)
        return EnvInfo(response["response"])

    def delete_env(self, env_name: str) -> None:
        self._execute(
            who_am_i(),
            envName=env_name
        )

    def clone_env(self, src_env_name: str, dst_env_name: str) -> EnvInfo:
        response = self._execute(
            who_am_i(), srcEnvName=src_env_name, dstEnvName=dst_env_name)
        return EnvInfo(response)

    def start_env(self, env_name: str) -> None:
        self._execute(who_am_i(), envName=env_name)

    def stop_env(self, env_name: str) -> None:
        self._execute(who_am_i(), envName=env_name)

    def get_env_info(self, env_name: str) -> EnvInfo:
        try:
            response = self._execute(
                who_am_i(),
                envName=env_name
            )
        except JelasticClientException as e:
            response = {
                "result": e.response["result"],
                "env": {
                    "status": EnvStatus.NotExists
                }
            }
        return EnvInfo(response)

    def get_container_env_vars_by_group(self, env_name: str, node_group: str) -> dict:
        response = self._execute(
            who_am_i(), envName=env_name, nodeGroup=node_group)
        return response["object"]

    def get_container_env_vars(self, env_name: str, node_id: int):
        response = self._execute(
            who_am_i(), envName=env_name, nodeId=node_id)
        return response["object"]

    def remove_container_env_vars(self, env_name: str, vars: [str], node_group: str = None, node_id: str = None):
        self._execute(
            who_am_i(), envName=env_name, nodeGroup=node_group, nodeId=node_id, vars=json.dumps(vars))

    def add_container_env_vars(self, env_name: str, vars: dict, node_group: str = None, node_id: int = None):
        self._execute(
            who_am_i(), envName=env_name, nodeGroup=node_group, nodeId=node_id, vars=json.dumps(vars))

    def set_container_env_vars(self, env_name: str, node_id: int, vars: [str]):
        self._execute(
            who_am_i(), envName=env_name, nodeId=node_id, vars=json.dumps(vars))

    def set_container_env_vars_by_group(self, env_name: str, node_group: str, vars: [str]):
        self._execute(
            who_am_i(), envName=env_name, nodeGroup=node_group, data=json.dumps(vars))

    @staticmethod
    def _create_random_env_name():
        env_id = "".join(random.choice(string.digits) for _ in range(7))
        return f"env-{env_id}"
