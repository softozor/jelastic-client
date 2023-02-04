import json
from typing import Optional

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
        success: Optional[dict] = None,
    ) -> str:
        try:
            file = open(filename, "r")
        except OSError:
            raise JelasticClientException(f"Unable to open file {filename}")

        with file:
            manifest_content = file.read()
            return self.install(
                manifest_content, env_name, settings, region=region, success=success
            )

    def install_from_url(
        self,
        url: str,
        env_name: Optional[str] = None,
        settings: Optional[dict] = None,
        region: Optional[str] = None,
        success: Optional[dict] = None,
    ) -> str:
        response = requests.get(url)
        if response.status_code != 200:
            raise JelasticClientException(f"Url not found: {url}")
        manifest_content = response.text
        return self.install(
            manifest_content, env_name, settings, region=region, success=success
        )

    def install(
        self,
        manifest_content: str,
        env_name: Optional[str] = None,
        settings: Optional[dict] = None,
        region: Optional[str] = None,
        success: Optional[dict] = None,
    ) -> str:
        """
        Install a custom JPS manifest.

        :param manifest_content: the content of the manifest file
        :param env_name: the environment name; it can only be empty (or None)
                         if the manifest is of type "install" and creates no nodes
        :param settings: the manifest settings
        :param region: the region where to install the manifest
                       (supported by the Jelastic provider)
        :param success: replacement for the success section in the input manifest
        :return: manifest success text
        """
        if success:
            manifest_content = self._replace_success_in_manifest(
                manifest_content, success
            )

        response = self._execute(
            who_am_i(),
            jps=manifest_content,
            envName=env_name,
            skipNodeEmails=True,
            settings=json.dumps(settings),
            region=region,
        )

        return response["successText"]

    @staticmethod
    def _replace_success_in_manifest(manifest_content: str, success: dict) -> str:
        manifest_data = yaml.safe_load(manifest_content)
        manifest_data["success"] = success
        updated_manifest_content = yaml.dump(manifest_data)
        return updated_manifest_content

    def get_engine_version(self) -> str:
        response = self._execute(who_am_i())

        return response["version"]
