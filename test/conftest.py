import random

import pytest

import jelastic_client
from random_helpers import random_env_name


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

# we don't random.seed here because otherwise we would not be able to run concurrent pipelines
# as concurrent pipeline would concurrently create environments with the same names


@pytest.fixture
def api_url(request):
    return request.config.getoption("--api-url")


@pytest.fixture
def api_token(request):
    return request.config.getoption("--api-token")


@pytest.fixture
def test_data_dir(request):
    return request.config.getoption("--test-data-dir")


@pytest.fixture
def supported_jelastic_version(request):
    return request.config.getoption("--jelastic-version")


@pytest.fixture
def client_factory(api_url, api_token):
    return jelastic_client.JelasticClientFactory(api_url, api_token)


@pytest.fixture
def jps_client(client_factory):
    return client_factory.create_jps_client()


@pytest.fixture
def control_client(client_factory):
    return client_factory.create_control_client()


@pytest.fixture
def new_env_name(control_client):
    env_name = random_env_name()
    while control_client.env_exists(env_name):
        env_name = random_env_name()
    yield env_name
    if control_client.env_exists(env_name):
        control_client.delete_env(env_name)


@pytest.fixture
def non_existent_env_name():
    return "non-existent-env"
