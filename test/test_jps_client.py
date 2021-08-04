import os


def test_jps_client_install_simple_manifest_returns_success_response(
        jps_client,
        test_data_dir,
        new_env_name):
    # Arrange
    filename = os.path.join(test_data_dir, "simple_manifest.jps")

    # Act
    response = jps_client.install(filename, new_env_name)

    # Assert
    assert response["result"] == 0
    assert response["response"]["result"] == 0

    # TODO: check that the environment is actually up and running
