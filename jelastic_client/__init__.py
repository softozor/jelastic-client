from .core import settings
from .jps_client import JpsClient

_api_client = None


def is_valid_api_client():
    from .core import ApiClient

    return isinstance(_api_client, ApiClient) \
           and _api_client.is_functional() \
           and _api_client.api_url == settings.api_url \
           and _api_client.api_token == settings.api_token


def define_api_client():
    from .core import ApiClient

    _api_client = ApiClient(api_url=settings.api_url, api_token=settings.api_token)

    return _api_client


def api_client():
    """
    Get the global api client
    """
    global _api_client

    if not is_valid_api_client():
        define_api_client()

    return _api_client
