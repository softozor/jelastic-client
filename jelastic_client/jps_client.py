from .core import ApiClient, BaseClient, JelasticClientException, success_response


class JpsClient(BaseClient):
    grp_cls = "marketplace.jps"

    def __init__(self, api_client: ApiClient):
        super().__init__(api_client)

    def install(self, filename: str, env_name: str) -> None:
        with open(filename) as file:
            manifest_content = file.read()

            response = self.execute(
                "Install",
                jps=manifest_content,
                envName=env_name
            )

            if not success_response(response):
                raise JelasticClientException(
                    f"installation of manifest {filename} failed", response)

    def get_engine_version(self) -> str:
        response = self.execute(
            "GetEngineVersion"
        )

        if not success_response(response):
            raise JelasticClientException(
                f"getting engine version failed", response)

        return response["version"]
