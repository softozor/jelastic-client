from .core import ApiClient, BaseClient


class JpsClient(BaseClient):
    jelastic_group = "marketplace"

    jelastic_class = "jps"

    def __init__(self, api_client: ApiClient):
        super().__init__(api_client)

    def install(self, filename: str, env_name: str) -> None:
        with open(filename) as file:
            manifest_content = file.read()

            self.execute(
                "Install",
                jps=manifest_content,
                envName=env_name
            )

    def get_engine_version(self) -> str:
        response = self.execute(
            "GetEngineVersion"
        )

        return response["version"]
