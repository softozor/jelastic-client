from enum import Enum
from typing import Dict

import simplejson as json

from .core import (
    ApiClient,
    BaseClient,
    ApiClientException,
    who_am_i
)
from .env_node import MultipleNodeSettings
from .env_settings import EnvSettings


class Status(Enum):
    Running = 1
    Down = 2
    Launching = 3
    Sleep = 4
    Unknown = 5
    Creating = 6
    Cloning = 7
    NotExists = 8
    Exporting = 9
    Migrating = 10
    Broken = 11
    Updating = 12
    Stopping = 13
    GoingToSleep = 14
    Restoring = 15


class ControlClient(BaseClient):
    jelastic_group = "environment"

    jelastic_class = "control"

    def __init__(self, api_client: ApiClient):
        super().__init__(api_client)

    def create_environment(self, env: EnvSettings, nodes: MultipleNodeSettings) -> str:
        env_json = json.dumps(env)
        nodes_json = json.dumps(nodes)
        response = self._execute(who_am_i(), env=env_json, nodes=nodes_json)
        return response["response"]["env"]["envName"]

    def delete_env(self, env_name: str) -> None:
        self._execute(
            who_am_i(),
            envName=env_name
        )

    def get_env_info(self, env_name: str) -> Dict:
        try:
            response = self._execute(
                who_am_i(),
                envName=env_name
            )
            return response
        except ApiClientException as e:
            return {
                "result": e.response["result"],
                "env": {
                    "status": Status.NotExists
                }
            }

    # TODO: we should probably have an EnvInfo class wrapping the response Dict with the following methods
    def env_is_running(self, env_name: str) -> bool:
        env_info = self.get_env_info(env_name)
        env_status = Status(env_info["env"]["status"])

        return env_status == Status.Running

    def env_exists(self, env_name: str) -> bool:
        env_info = self.get_env_info(env_name)
        env_status = Status(env_info["env"]["status"])

        return env_status is not Status.NotExists and env_status is not Status.Unknown

    # TODO: test this:
    #   1. create_env -> return env info
    #   2. from env info, we know what (intIP, nodeGroup, nodeType) we have (given a nodeGroup, we know what intIPs to expect for example)
    #   3. confront get_node_ips with the previously obtained env info
    # - given a nodeGroup, fetch the related IPs
    # - given a nodeType, fetch the related IPs
    # - give a nodeType AND a nodeGroup, fetch the related IPs
    def get_node_ips(self, env_name: str, node_group: str = None, node_type: str = None) -> list[str]:
        env_info = self.get_env_info(env_name)
        env_nodes = env_info["nodes"]

        node_ips_with_node_group = []
        if node_group is not None:
            node_ips_with_node_group = [env_node["intIP"] for env_node in env_nodes if
                                        env_node["nodeGroup"] == node_group]
            if node_type is None:
                return node_ips_with_node_group

        node_ips_with_node_type = []
        if node_type is not None:
            node_ips_with_node_type = [
                env_node["intIP"] for env_node in env_nodes if env_node["nodeType"] == node_type]
            if node_group is None:
                return node_ips_with_node_type

        return list(set(node_ips_with_node_type).intersection(node_ips_with_node_group))
