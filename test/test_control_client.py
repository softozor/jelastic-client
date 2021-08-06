import pytest

from jelastic_client import ControlClient
from jelastic_client.core import JelasticClientException


def test_control_client_delete_non_existent_environment_raises_exception(
        control_client: ControlClient,
        non_existent_env_name: str):
    # Arrange

    # Act / Assert
    with pytest.raises(JelasticClientException):
        control_client.delete_env(non_existent_env_name)
