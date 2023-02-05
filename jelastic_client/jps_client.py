import json
from typing import Dict, Optional, Union

import requests  # type: ignore
import yaml  # type: ignore

from .core import ApiClient, BaseClient, JelasticClientException, who_am_i


class JpsClient(BaseClient):
    jelastic_group = "marketplace"

    jelastic_class = "jps"

    def __init__(self, api_client: ApiClient):
        super().__init__(api_client)

    def install_from_file(
        self,
        filename: str,
        env_name: Optional[str] = None,
        settings: Optional[dict] = None,
        region: Optional[str] = None,
        env_props_query: Optional[dict] = None,
    ) -> Union[str, Dict[str, str]]:
        try:
            file = open(filename, "r")
        except OSError:
            raise JelasticClientException(f"Unable to open file {filename}")

        with file:
            manifest_content = file.read()
            return self.install(
                manifest_content,
                env_name,
                settings,
                region=region,
                env_props_query=env_props_query,
            )

    def install_from_url(
        self,
        url: str,
        env_name: Optional[str] = None,
        settings: Optional[dict] = None,
        region: Optional[str] = None,
        env_props_query: Optional[dict] = None,
    ) -> Union[str, Dict[str, str]]:
        response = requests.get(url)
        if response.status_code != 200:
            raise JelasticClientException(f"Url not found: {url}")
        manifest_content = response.text
        return self.install(
            manifest_content,
            env_name,
            settings,
            region=region,
            env_props_query=env_props_query,
        )

    # TODO: add the following arguments:
    # - send_node_emails: bool
    # - send_success_email: bool
    def install(
        self,
        manifest_content: str,
        env_name: Optional[str] = None,
        settings: Optional[dict] = None,
        region: Optional[str] = None,
        env_props_query: Optional[dict] = None,
    ) -> Union[str, Dict[str, str]]:
        """
        Install a custom JPS manifest.

        :param manifest_content: the content of the manifest file
        :param env_name: the environment name; it can only be empty (or None)
                         if the manifest is of type "install" and creates no nodes
        :param settings: the manifest settings
        :param region: the region where to install the manifest
                       (supported by the Jelastic provider)
        :param env_props_query: set of (key, value) to query an installation about
            e.g. ("AdminPassword", "${nodes.sqldb.password}")
        :return: manifest success text if no env_props_query was provided,
                 else the set of (key, value) corresponding to the env_props_query
        """
        if env_props_query:
            manifest_content = self._apply_env_props_query(
                manifest_content, env_props_query
            )

        response = self._execute(
            who_am_i(),
            jps=manifest_content,
            envName=env_name,
            skipNodeEmails=True,
            settings=json.dumps(settings),
            region=region,
        )

        return (
            self._get_env_props(response["successText"])
            if env_props_query
            else response["successText"]
        )

    # TODO: the separator ", " should be somehow stored somewhere
    @staticmethod
    def _apply_env_props_query(
        manifest_content: str, env_props_query: Dict[str, str]
    ) -> str:
        manifest_data = yaml.safe_load(manifest_content)
        manifest_data["success"] = {
            "email": False,
            "text": ", ".join(
                f"{key}: {value}" for key, value in env_props_query.items()
            ),
        }
        updated_manifest_content = yaml.dump(manifest_data)
        return updated_manifest_content

    # TODO: the separator ", " should be somehow stored somewhere
    @staticmethod
    def _get_env_props(response: str) -> Dict[str, str]:
        items = response.split(", ")
        return {item.split(": ")[0]: item.split(": ")[1] for item in items}

    def get_engine_version(self) -> str:
        response = self._execute(who_am_i())
        return response["version"]
