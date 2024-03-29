import os
import random
import sys
from test.utils import get_new_random_env_name
from typing import Generator, Tuple, TypeVar

import pytest
import requests  # type: ignore
from _pytest.fixtures import FixtureRequest

from jelastic_client import (
    AccountClient,
    ControlClient,
    DockerSettings,
    EnvInfo,
    EnvSettings,
    FileClient,
    JelasticClientFactory,
    JpsClient,
    NodeSettings,
)

here = os.path.dirname(os.path.abspath(__file__))

T = TypeVar("T")

YieldFixture = Generator[T, None, None]


def pytest_addoption(parser):
    parser.addoption(
        "--api-url",
        action="store",
        default="https://app.hidora.com/1.0",
        help="jelastic api url",
    )
    parser.addoption(
        "--api-token", action="store", required=True, help="jelastic access token"
    )
    parser.addoption(
        "--base-url",
        action="store",
        default="https://raw.githubusercontent.com/softozor/jelastic-client/main/",
        help="project base url for raw files",
    )
    parser.addoption(
        "--jelastic-version",
        action="store",
        required=True,
        help="supported jelastic version",
    )
    parser.addoption(
        "--commit-sha",
        action="store",
        required=True,
        help="commit short sha (8 characters)",
    )
    parser.addoption(
        "--jelastic-user-email",
        action="store",
        required=True,
        help="email of Jelastic user account",
    )


@pytest.fixture(autouse=True, scope="session")
def random_seed() -> None:
    random.seed(
        f"softozor/jelastic-client/py-{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    )


@pytest.fixture
def api_url(request: FixtureRequest) -> str:
    return request.config.getoption("--api-url")


@pytest.fixture
def api_token(request: FixtureRequest) -> str:
    return request.config.getoption("--api-token")


@pytest.fixture
def base_url(request: FixtureRequest) -> str:
    return request.config.getoption("--base-url")


@pytest.fixture
def jelastic_user_email(request: FixtureRequest) -> str:
    return request.config.getoption("--jelastic-user-email")


@pytest.fixture
def supported_jelastic_version(request: FixtureRequest) -> str:
    return request.config.getoption("--jelastic-version")


@pytest.fixture
def commit_sha(request: FixtureRequest) -> str:
    return request.config.getoption("--commit-sha")


@pytest.fixture
def valid_manifest_file() -> str:
    return os.path.join(here, "data", "valid_manifest.jps")


@pytest.fixture
def valid_manifest_url(base_url) -> str:
    url = f"{base_url}/test/data/valid_manifest.jps"
    response = requests.get(url)
    assert 200 == response.status_code
    return url


@pytest.fixture
def valid_update_manifest_url(base_url) -> str:
    url = f"{base_url}/test/data/valid_update_manifest.jps"
    response = requests.get(url)
    assert 200 == response.status_code
    return url


@pytest.fixture
def manifest_file_with_settings() -> str:
    return os.path.join(here, "data", "manifest_with_settings.jps")


@pytest.fixture
def manifest_url_with_settings(base_url) -> str:
    url = f"{base_url}/test/data/manifest_with_settings.jps"
    response = requests.get(url)
    assert 200 == response.status_code
    return url


@pytest.fixture
def invalid_manifest_file() -> str:
    return os.path.join(here, "data", "invalid_manifest.jps")


@pytest.fixture
def invalid_manifest_url(base_url) -> str:
    url = f"{base_url}/test/data/invalid_manifest.jps"
    response = requests.get(url)
    assert 200 == response.status_code
    return url


@pytest.fixture
def non_existent_manifest_file() -> str:
    filename = os.path.join(here, "data", "non_existent_manifest.jps")
    assert not os.path.exists(filename)
    return filename


@pytest.fixture
def non_existent_manifest_url(base_url) -> str:
    url = f"{base_url}/test/data/non_existent_manifest.jps"
    response = requests.get(url)
    assert 404 == response.status_code
    return url


@pytest.fixture
def client_factory(api_url: str, api_token: str) -> JelasticClientFactory:
    return JelasticClientFactory(api_url, api_token)


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
def account_client(client_factory: JelasticClientFactory) -> AccountClient:
    return client_factory.create_account_client()


@pytest.fixture
def new_env_name(
    control_client: ControlClient, commit_sha: str, worker_id: str
) -> YieldFixture[str]:
    env_name = get_new_random_env_name(control_client, commit_sha, worker_id)
    yield env_name
    env_info = control_client.get_env_info(env_name)
    if env_info.exists():
        control_client.delete_env(env_name)


@pytest.fixture
def created_environment(
    control_client: ControlClient, new_env_name: str
) -> YieldFixture[EnvInfo]:
    env = EnvSettings(shortdomain=new_env_name)
    sql_node = NodeSettings(
        fixedCloudlets=3, flexibleCloudlets=4, nodeType="postgresql"
    )
    docker_settings = DockerSettings(image="alpine")
    docker_node = NodeSettings(
        docker=docker_settings, flexibleCloudlets=4, nodeType="docker"
    )
    env_info = control_client.create_environment(env, [sql_node, docker_node])
    yield env_info
    env_info = control_client.get_env_info(new_env_name)
    if env_info.exists():
        control_client.delete_env(new_env_name)


@pytest.fixture
def cloned_environment(
    control_client: ControlClient, created_environment: EnvInfo
) -> YieldFixture[EnvInfo]:
    created_env_name = created_environment.env_name()
    cloned_env_name = created_env_name + "-clone"
    env_info = control_client.clone_env(created_env_name, cloned_env_name)
    yield env_info
    env_info = control_client.get_env_info(cloned_env_name)
    if env_info.exists():
        control_client.delete_env(cloned_env_name)


@pytest.fixture
def valid_environment_with_env_vars(
    jps_client: JpsClient,
    control_client: ControlClient,
    new_env_name: str,
    valid_manifest_file: str,
) -> YieldFixture[str]:
    jps_client.install_from_file(valid_manifest_file, new_env_name)
    yield new_env_name
    env_info = control_client.get_env_info(new_env_name)
    if env_info.exists():
        control_client.delete_env(new_env_name)


@pytest.fixture
def non_existent_env_name() -> str:
    return "non-existent-env"


@pytest.fixture
def alpine_with_file(
    control_client: ControlClient, new_env_name: str
) -> Tuple[str, str]:
    env = EnvSettings(shortdomain=new_env_name)
    docker_settings = DockerSettings(image="softozor/alpine-with-file:latest")
    node = NodeSettings(docker=docker_settings, flexibleCloudlets=4, nodeType="docker")
    control_client.create_environment(env, [node])
    return new_env_name, "/app/file.txt"


@pytest.fixture
def expected_file_content_in_alpine_with_file() -> str:
    with open(
        os.path.join(here, "docker", "alpine-with-file", "file.txt"), "r"
    ) as file:
        return file.read()
