import os

import pytest

from jelastic_client import ControlClient
from jelastic_client.core.exceptions import JelasticClientException


def test_jps_client_install_valid_manifest_puts_up_environment(
        control_client: ControlClient,
        jps_client,
        test_data_dir,
        new_env_name):
    # Arrange
    filename = os.path.join(test_data_dir, "valid_manifest.jps")

    # Act
    jps_client.install(filename, new_env_name)

    # Assert
    assert control_client.env_is_running(new_env_name)


def test_jps_client_install_invalid_manifest_raises_exception(
        jps_client,
        test_data_dir,
        new_env_name):
    # Arrange
    filename = os.path.join(test_data_dir, "invalid_manifest.jps")

    # Act / Assert
    with pytest.raises(JelasticClientException):
        jps_client.install(filename, new_env_name)
