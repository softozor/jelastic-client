import os

import pytest

from jelastic_client import ControlClient, JpsClient
from jelastic_client.core.exceptions import JelasticClientException


def test_jps_client_install_from_file_valid_manifest_creates_environment(
        control_client: ControlClient,
        jps_client: JpsClient,
        test_data_dir: str,
        new_env_name: str):
    # Arrange
    filename = os.path.join(test_data_dir, "valid_manifest.jps")

    # Act
    jps_client.install_from_file(filename, new_env_name)

    # Assert
    env_info = control_client.get_env_info(new_env_name)
    assert env_info.exists()


def test_jps_client_install_from_file_valid_manifest_makes_environment_run(
        control_client: ControlClient,
        jps_client: JpsClient,
        test_data_dir: str,
        new_env_name: str):
    # Arrange
    filename = os.path.join(test_data_dir, "valid_manifest.jps")

    # Act
    jps_client.install_from_file(filename, new_env_name)

    # Assert
    env_info = control_client.get_env_info(new_env_name)
    assert env_info.is_running()


def test_jps_client_install_from_file_valid_manifest_returns_success_text(
        jps_client: JpsClient,
        test_data_dir: str,
        new_env_name: str):
    # Arrange
    filename = os.path.join(test_data_dir, "valid_manifest.jps")

    # Act
    actual_success_text = jps_client.install_from_file(filename, new_env_name)

    # Assert
    expected_success_text = "<strong>Field1</strong>: Value1\n<strong>Field2</strong>: Value2"
    assert expected_success_text == actual_success_text


def test_jps_client_install_from_file_invalid_manifest_raises_exception(
        jps_client: JpsClient,
        test_data_dir: str,
        new_env_name: str):
    # Arrange
    filename = os.path.join(test_data_dir, "invalid_manifest.jps")

    # Act / Assert
    with pytest.raises(JelasticClientException):
        jps_client.install_from_file(filename, new_env_name)


def test_jps_client_install_from_file_non_existent_manifest_raises_exception(
        jps_client: JpsClient,
        test_data_dir: str,
        new_env_name: str):
    # Arrange
    filename = os.path.join(test_data_dir, "non_existent_manifest.jps")
    assert not os.path.exists(filename)

    # Act / Assert
    with pytest.raises(OSError):
        jps_client.install_from_file(filename, new_env_name)


def test_jps_client_get_engine_version_returns_supported_engine_version(
        jps_client: JpsClient,
        supported_jelastic_version: str):
    # Arrange

    # Act
    actual_version = jps_client.get_engine_version()

    # Assert
    assert supported_jelastic_version == actual_version
