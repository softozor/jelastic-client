import pytest

from jelastic_client import ControlClient, JelasticClientException, JpsClient


def test_jps_client_install_from_file_valid_manifest_file_creates_environment(
    control_client: ControlClient,
    jps_client: JpsClient,
    valid_manifest_file: str,
    new_env_name: str,
):
    # Arrange

    # Act
    jps_client.install_from_file(valid_manifest_file, new_env_name)

    # Assert
    env_info = control_client.get_env_info(new_env_name)
    assert env_info.exists()


def test_jps_client_install_from_url_valid_manifest_url_creates_environment(
    control_client: ControlClient,
    jps_client: JpsClient,
    valid_manifest_url: str,
    new_env_name: str,
):
    # Arrange

    # Act
    jps_client.install_from_url(valid_manifest_url, new_env_name)

    # Assert
    env_info = control_client.get_env_info(new_env_name)
    assert env_info.exists()


def test_jps_client_install_from_file_valid_manifest_file_makes_environment_run(
    control_client: ControlClient,
    jps_client: JpsClient,
    valid_manifest_file: str,
    new_env_name: str,
):
    # Arrange

    # Act
    jps_client.install_from_file(valid_manifest_file, new_env_name)

    # Assert
    env_info = control_client.get_env_info(new_env_name)
    assert env_info.is_running()


def test_jps_client_install_from_url_valid_manifest_url_makes_environment_run(
    control_client: ControlClient,
    jps_client: JpsClient,
    valid_manifest_url: str,
    new_env_name: str,
):
    # Arrange

    # Act
    jps_client.install_from_url(valid_manifest_url, new_env_name)

    # Assert
    env_info = control_client.get_env_info(new_env_name)
    assert env_info.is_running()


def test_jps_client_install_from_file_valid_manifest_file_returns_success_text(
    jps_client: JpsClient, valid_manifest_file: str, new_env_name: str
):
    # Arrange

    # Act
    actual_success_text = jps_client.install_from_file(
        valid_manifest_file, new_env_name
    )

    # Assert
    expected_success_text = (
        "<strong>Field1</strong>: Value1<br />\n<strong>Field2</strong>: Value2"
    )
    assert expected_success_text == actual_success_text


def test_jps_client_install_from_url_valid_manifest_url_returns_success_text(
    jps_client: JpsClient, valid_manifest_url: str, new_env_name: str
):
    # Arrange

    # Act
    actual_success_text = jps_client.install_from_url(valid_manifest_url, new_env_name)

    # Assert
    expected_success_text = (
        "<strong>Field1</strong>: Value1<br />\n<strong>Field2</strong>: Value2"
    )
    assert expected_success_text == actual_success_text


def test_jps_client_install_from_valid_manifest_url_with_env_props_query_returns_expected_env_props(
    jps_client: JpsClient, manifest_url_with_settings: str
):
    # Arrange
    env_props_query = {
        "first field": "${settings.field1}",
        "second field": "${settings.field2}",
    }
    settings = {"field1": "value1", "field2": "value2"}

    # Act
    actual_env_props = jps_client.install_from_url(
        manifest_url_with_settings, env_props_query=env_props_query, settings=settings
    )

    # Assert
    expected_env_props = {
        "first field": "value1",
        "second field": "value2",
    }
    assert actual_env_props == expected_env_props


def test_jps_client_install_from_valid_manifest_file_with_env_props_query_returns_expected_env_props(
    jps_client: JpsClient, manifest_file_with_settings: str
):
    # Arrange
    env_props_query = {
        "first field": "${settings.field1}",
        "second field": "${settings.field2}",
    }
    settings = {"field1": "value1", "field2": "value2"}

    # Act
    actual_env_props = jps_client.install_from_file(
        manifest_file_with_settings, env_props_query=env_props_query, settings=settings
    )

    # Assert
    expected_env_props = {
        "first field": "value1",
        "second field": "value2",
    }
    assert actual_env_props == expected_env_props


def test_jps_client_install_from_file_invalid_manifest_file_raises_exception(
    jps_client: JpsClient, invalid_manifest_file: str, new_env_name: str
):
    # Arrange

    # Act / Assert
    with pytest.raises(JelasticClientException):
        jps_client.install_from_file(invalid_manifest_file, new_env_name)


def test_jps_client_install_from_url_invalid_manifest_url_raises_exception(
    jps_client: JpsClient, invalid_manifest_url: str, new_env_name: str
):
    # Arrange

    # Act / Assert
    with pytest.raises(JelasticClientException):
        jps_client.install_from_url(invalid_manifest_url, new_env_name)


def test_jps_client_install_from_file_non_existent_manifest_file_raises_exception(
    jps_client: JpsClient, non_existent_manifest_file: str, new_env_name: str
):
    # Arrange

    # Act / Assert
    with pytest.raises(JelasticClientException):
        jps_client.install_from_file(non_existent_manifest_file, new_env_name)


def test_jps_client_install_from_url_non_existent_manifest_url_raises_exception(
    jps_client: JpsClient, non_existent_manifest_url: str, new_env_name: str
):
    # Arrange

    # Act / Assert
    with pytest.raises(JelasticClientException):
        jps_client.install_from_url(non_existent_manifest_url, new_env_name)


def test_jps_client_install_environment_with_nodes_but_no_env_name_provided_throws(
    jps_client: JpsClient, valid_manifest_url: str
):
    # Arrange

    # Act / Assert
    with pytest.raises(JelasticClientException):
        jps_client.install_from_url(valid_manifest_url)


def test_jps_client_update_environment_but_no_env_name_provided_throws(
    jps_client: JpsClient, valid_update_manifest_url: str
):
    # Arrange

    # Act / Assert
    with pytest.raises(JelasticClientException):
        jps_client.install_from_url(valid_update_manifest_url)


def test_jps_client_get_engine_version_returns_supported_engine_version(
    jps_client: JpsClient, supported_jelastic_version: str
):
    # Arrange

    # Act
    actual_version = jps_client.get_engine_version()

    # Assert
    assert supported_jelastic_version == actual_version


def test_jps_client_install_from_url_valid_manifest_url_returns_installs_in_region_sh1(
    control_client: ControlClient,
    jps_client: JpsClient,
    valid_manifest_url: str,
    new_env_name: str,
):
    # Arrange
    expected_domain = f"{new_env_name}.sh1.hidora.com"

    # Act
    jps_client.install_from_url(valid_manifest_url, new_env_name, region="sh1")

    # Assert
    env_info = control_client.get_env_info(new_env_name)
    assert expected_domain == env_info.domain()


def test_jps_client_install_from_url_valid_manifest_url_returns_installs_in_region_new(
    control_client: ControlClient,
    jps_client: JpsClient,
    valid_manifest_url: str,
    new_env_name: str,
):
    # Arrange
    expected_domain = f"{new_env_name}.hidora.com"

    # Act
    jps_client.install_from_url(valid_manifest_url, new_env_name, region="new")

    # Assert
    env_info = control_client.get_env_info(new_env_name)
    assert expected_domain == env_info.domain()


def test_jps_client_install_from_file_valid_manifest_file_installs_in_region_sh1(
    control_client: ControlClient,
    jps_client: JpsClient,
    valid_manifest_file: str,
    new_env_name: str,
):
    # Arrange
    expected_domain = f"{new_env_name}.sh1.hidora.com"

    # Act
    jps_client.install_from_file(valid_manifest_file, new_env_name, region="sh1")

    # Assert
    env_info = control_client.get_env_info(new_env_name)
    assert expected_domain == env_info.domain()


def test_jps_client_install_from_file_valid_manifest_file_installs_in_region_new(
    control_client: ControlClient,
    jps_client: JpsClient,
    valid_manifest_file: str,
    new_env_name: str,
):
    # Arrange
    expected_domain = f"{new_env_name}.hidora.com"

    # Act
    jps_client.install_from_file(valid_manifest_file, new_env_name, region="new")

    # Assert
    env_info = control_client.get_env_info(new_env_name)
    assert expected_domain == env_info.domain()
