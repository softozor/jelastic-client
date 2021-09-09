import os
import random

import pytest
from _pytest.fixtures import FixtureRequest

import jelastic_client
from jelastic_client import (
    JelasticClientFactory,
    JpsClient,
    ControlClient,
    FileClient,
    EnvSettings,
    DockerSettings,
    NodeSettings
)
from test_utils import get_new_random_env_name


def pytest_addoption(parser):
    parser.addoption(
        "--api-url", action="store", default="https://app.hidora.com/1.0", help="jelastic api url"
    )
    parser.addoption(
        "--api-token", action="store", required=True, help="jelastic access token"
    )
    parser.addoption(
        "--test-data-dir", action="store", default="./data", help="path to test data folder"
    )
    parser.addoption(
        "--jelastic-version", action="store", required=True, help="supported jelastic version"
    )
    parser.addoption(
        "--commit-sha", action="store", required=True, help="commit short sha (8 characters)"
    )


@pytest.fixture(autouse=True, scope="session")
def random_seed() -> None:
    random.seed("jelastic-client-integration-tests")


@pytest.fixture
def api_url(request: FixtureRequest) -> str:
    return request.config.getoption("--api-url")


@pytest.fixture
def api_token(request: FixtureRequest) -> str:
    return request.config.getoption("--api-token")


@pytest.fixture
def test_data_dir(request: FixtureRequest) -> str:
    return request.config.getoption("--test-data-dir")


@pytest.fixture
def valid_manifest(test_data_dir) -> str:
    return os.path.join(test_data_dir, "valid_manifest.jps")


@pytest.fixture
def manifest_with_settings(test_data_dir) -> str:
    return os.path.join(test_data_dir, "manifest_with_settings.jps")


@pytest.fixture
def invalid_manifest(test_data_dir) -> str:
    return os.path.join(test_data_dir, "invalid_manifest.jps")


@pytest.fixture
def non_existent_manifest(test_data_dir) -> str:
    filename = os.path.join(test_data_dir, "non_existent_manifest.jps")
    assert not os.path.exists(filename)
    return filename


@pytest.fixture
def supported_jelastic_version(request: FixtureRequest) -> str:
    return request.config.getoption("--jelastic-version")


@pytest.fixture
def commit_sha(request: FixtureRequest) -> str:
    return request.config.getoption("--commit-sha")


@pytest.fixture
def client_factory(api_url: str, api_token: str) -> JelasticClientFactory:
    return jelastic_client.JelasticClientFactory(api_url, api_token)


@pytest.fixture
def jps_client(client_factory: JelasticClientFactory) -> JpsClient:
    return client_factory.create_jps_client()


@pytest.fixture
def control_client(client_factory: JelasticClientFactory) -> ControlClient:
    return client_factory.create_control_client()


@pytest.fixture
def file_client(client_factory: JelasticClientFactory) -> FileClient:
    return client_factory.create_file_client()


@pytest.fixture
def new_env_name(control_client: ControlClient, commit_sha: str, worker_id: str) -> str:
    env_name = get_new_random_env_name(control_client, commit_sha, worker_id)
    yield env_name
    env_info = control_client.get_env_info(env_name)
    if env_info.exists():
        control_client.delete_env(env_name)


@pytest.fixture
def non_existent_env_name() -> str:
    return "non-existent-env"


@pytest.fixture
def alpine_with_file(control_client: ControlClient, new_env_name: str) -> tuple[str, str]:
    env = EnvSettings(shortdomain=new_env_name)
    docker_settings = DockerSettings(image="softozor/alpine-with-file:latest")
    node = NodeSettings(docker=docker_settings,
                        flexibleCloudlets=4, nodeType="docker")
    control_client.create_environment(env, [node])
    return new_env_name, "/app/file.txt"


@pytest.fixture
def expected_file_content_in_alpine_with_file() -> str:
    with open(os.path.join("./docker", "alpine-with-file", "file.txt"), "r") as file:
        return file.read()
