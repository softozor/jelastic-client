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


@pytest.fixture(autouse=True, scope="session")
def random_seed():
    random.seed('jelastic-client')


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
    yield env_name
    if control_client.env_exists(env_name):
        control_client.delete_env(env_name)
