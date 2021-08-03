import pytest

import jelastic_client


def pytest_addoption(parser):
    parser.addoption(
        "--api-url", action="store", default="https://app.hidora.com", help="jelastic api url"
    )
    parser.addoption(
        "--api-token", action="store", required=True, help="jelastic access token"
    )


@pytest.fixture
def api_url(request):
    return request.config.getoption("--api-url")


@pytest.fixture
def api_token(request):
    return request.config.getoption("--api-token")


@pytest.fixture
def client_factory(api_url, api_token):
    return jelastic_client.JelasticClientFactory(api_url, api_token)


@pytest.fixture
def jps_client(client_factory):
    return client_factory.create_jps_client()
