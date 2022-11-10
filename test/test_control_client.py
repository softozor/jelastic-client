import json
import re

import pytest

from jelastic_client import ControlClient, NodeSettings, EnvSettings, DockerSettings
from jelastic_client.core import JelasticClientException
from jelastic_client.env_info import EnvInfo


def test_generate_random_env_name_follows_jelastic_string_pattern(
    control_client: ControlClient,
):
    # Arrange

    # Act
    env_name = control_client.generate_random_env_name()

    # Assert
    pattern = re.compile("^env-[0-9]{7}$")
    assert pattern.match(env_name)


def test_control_client_delete_non_existent_environment_raises_exception(
    control_client: ControlClient, non_existent_env_name: str
):
    # Arrange

    # Act / Assert
    with pytest.raises(JelasticClientException):
        control_client.delete_env(non_existent_env_name)


def test_control_client_create_environment_with_single_vps_node_runs_environment(
    control_client: ControlClient, new_env_name: str
):
    # Arrange
    env = EnvSettings(shortdomain=new_env_name)
    node = NodeSettings(flexibleCloudlets=4, nodeType="ubuntu-vps")

    # Act
    created_env_info = control_client.create_environment(env, [node])

    # Assert
    actual_env_name = created_env_info.env_name()
    assert new_env_name == actual_env_name
    actual_env_info = control_client.get_env_info(actual_env_name)
    assert actual_env_info.is_running()


def test_control_client_create_environment_with_single_sql_node_runs_environment(
    control_client: ControlClient, new_env_name: str
):
    # Arrange
    env = EnvSettings(shortdomain=new_env_name)
    # postgres needs at least 3 cloudlets
    node = NodeSettings(fixedCloudlets=3, flexibleCloudlets=4, nodeType="postgresql")

    # Act
    created_env_info = control_client.create_environment(env, [node])

    # Assert
    actual_env_name = created_env_info.env_name()
    assert new_env_name == actual_env_name
    actual_env_info = control_client.get_env_info(actual_env_name)
    assert actual_env_info.is_running()


def test_control_client_create_environment_with_single_docker_node_runs_environment(
    control_client: ControlClient, new_env_name: str
):
    # Arrange
    env = EnvSettings(shortdomain=new_env_name)
    docker_settings = DockerSettings(image="alpine")
    node = NodeSettings(docker=docker_settings, flexibleCloudlets=4, nodeType="docker")

    # Act
    created_env_info = control_client.create_environment(env, [node])

    # Assert
    actual_env_name = created_env_info.env_name()
    assert new_env_name == actual_env_name
    actual_env_info = control_client.get_env_info(actual_env_name)
    assert actual_env_info.is_running()


def test_control_client_create_environment_with_multiple_nodes_runs_environment(
    control_client: ControlClient, new_env_name: str
):
    # Arrange
    env = EnvSettings(shortdomain=new_env_name)
    # postgres needs at least 3 cloudlets
    sql_node = NodeSettings(
        fixedCloudlets=3, flexibleCloudlets=4, nodeType="postgresql"
    )
    docker_settings = DockerSettings(image="alpine")
    docker_node = NodeSettings(
        docker=docker_settings, flexibleCloudlets=4, nodeType="docker"
    )

    # Act
    created_env_info = control_client.create_environment(env, [sql_node, docker_node])

    # Assert
    actual_env_name = created_env_info.env_name()
    assert new_env_name == actual_env_name
    actual_env_info = control_client.get_env_info(actual_env_name)
    assert actual_env_info.is_running()


def test_control_client_clone_environment_runs_cloned_environment(
    control_client: ControlClient,
    created_environment: EnvInfo,
    cloned_environment: EnvInfo,
):
    # Arrange

    # Act

    # Assert
    assert cloned_environment.is_running()
    assert len(created_environment.nodes()) == len(cloned_environment.nodes())


def test_control_client_start_stopped_environment(
    control_client: ControlClient, created_environment: EnvInfo
):
    # Arrange
    assert created_environment.is_running()
    env_name = created_environment.env_name()
    control_client.stop_env(env_name)
    env_info = control_client.get_env_info(env_name)
    assert not env_info.is_running()

    # Act
    control_client.start_env(env_name)

    # Assert
    env_info = control_client.get_env_info(env_name)
    assert env_info.is_running()


def test_control_client_get_container_env_vars_by_group_can_return_json_env_var(
    control_client: ControlClient, valid_environment_with_env_vars: str
):
    # Arrange

    # Act
    actual_env_vars = control_client.get_container_env_vars_by_group(
        valid_environment_with_env_vars, "cp"
    )
    actual_json_env_var = actual_env_vars["MY_JSON_VAR"]
    actual_json_value = json.loads(actual_json_env_var)

    # Assert
    assert len(actual_env_vars) > 1
    assert (
        "test" == actual_json_value["type"]
    ), f'expected "test", got {actual_json_value["type"]}'
    assert ["app-1", "app-2"] == actual_json_value[
        "audience"
    ], f'expected {["app-1", "app-2"]}, got {actual_json_value["audience"]}'


def test_control_client_get_container_env_vars_can_return_json_env_var(
    control_client: ControlClient, valid_environment_with_env_vars: str
):
    # Arrange
    env_info = control_client.get_env_info(valid_environment_with_env_vars)
    cp_node = env_info.get_nodes(node_group="cp")[0]
    cp_node_id = cp_node.id

    # Act
    actual_env_vars = control_client.get_container_env_vars(
        valid_environment_with_env_vars, cp_node_id
    )
    actual_json_env_var = actual_env_vars["MY_JSON_VAR"]
    actual_json_value = json.loads(actual_json_env_var)

    # Assert
    assert len(actual_env_vars) > 1
    assert (
        "test" == actual_json_value["type"]
    ), f'expected "test", got {actual_json_value["type"]}'
    assert ["app-1", "app-2"] == actual_json_value[
        "audience"
    ], f'expected {["app-1", "app-2"]}, got {actual_json_value["audience"]}'


def test_control_client_remove_container_env_vars_removes_one_single_var(
    control_client: ControlClient, valid_environment_with_env_vars: str
):
    # Arrange
    vars_to_remove = ["MY_OTHER_VAR"]

    # Act
    control_client.remove_container_env_vars(
        valid_environment_with_env_vars, vars=vars_to_remove, node_group="cp"
    )
    actual_env_vars = control_client.get_container_env_vars_by_group(
        valid_environment_with_env_vars, "cp"
    )

    # Assert
    assert "MY_OTHER_VAR" not in actual_env_vars


def test_control_client_remove_container_env_vars_removes_multiple_vars(
    control_client: ControlClient, valid_environment_with_env_vars: str
):
    # Arrange
    vars_to_remove = ["MY_OTHER_VAR", "MY_JSON_VAR"]

    # Act
    control_client.remove_container_env_vars(
        valid_environment_with_env_vars, vars=vars_to_remove, node_group="cp"
    )
    actual_env_vars = control_client.get_container_env_vars_by_group(
        valid_environment_with_env_vars, "cp"
    )

    # Assert
    assert "MY_OTHER_VAR" not in actual_env_vars
    assert "MY_JSON_VAR" not in actual_env_vars


def test_control_client_remove_container_env_vars_is_no_op_when_non_existent_variable(
    control_client: ControlClient, valid_environment_with_env_vars: str
):
    # Arrange
    initial_env_vars = control_client.get_container_env_vars_by_group(
        valid_environment_with_env_vars, "cp"
    )
    vars_to_remove = ["MY_NON_EXISTENT_VAR"]
    assert vars_to_remove[0] not in initial_env_vars

    # Act
    control_client.remove_container_env_vars(
        valid_environment_with_env_vars, vars=vars_to_remove, node_group="cp"
    )
    actual_env_vars = control_client.get_container_env_vars_by_group(
        valid_environment_with_env_vars, "cp"
    )

    # Assert
    assert initial_env_vars == actual_env_vars


def test_control_client_add_container_env_vars(
    control_client: ControlClient, valid_environment_with_env_vars: str
):
    # Arrange
    vars_to_add = {"MY_FIRST_NEW_VAR": "value1", "MY_SECOND_NEW_VAR": "value2"}

    # Act
    control_client.add_container_env_vars(
        valid_environment_with_env_vars, vars=vars_to_add, node_group="cp"
    )
    actual_env_vars = control_client.get_container_env_vars_by_group(
        valid_environment_with_env_vars, "cp"
    )

    # Assert
    assert "MY_FIRST_NEW_VAR" in actual_env_vars
    assert "MY_SECOND_NEW_VAR" in actual_env_vars
    assert vars_to_add["MY_FIRST_NEW_VAR"] == actual_env_vars["MY_FIRST_NEW_VAR"]
    assert vars_to_add["MY_SECOND_NEW_VAR"] == actual_env_vars["MY_SECOND_NEW_VAR"]


def test_control_client_add_container_env_vars_overwrites_already_existing_variable(
    control_client: ControlClient, valid_environment_with_env_vars: str
):
    # Arrange
    initial_env_vars = control_client.get_container_env_vars_by_group(
        valid_environment_with_env_vars, "cp"
    )
    vars_to_add = {
        "MY_OTHER_VAR": "value1",
    }
    assert "MY_OTHER_VAR" in initial_env_vars
    assert initial_env_vars["MY_OTHER_VAR"] != vars_to_add["MY_OTHER_VAR"]

    # Act
    control_client.add_container_env_vars(
        valid_environment_with_env_vars, vars=vars_to_add, node_group="cp"
    )
    actual_env_vars = control_client.get_container_env_vars_by_group(
        valid_environment_with_env_vars, "cp"
    )

    # Assert
    assert "MY_OTHER_VAR" in actual_env_vars
    assert vars_to_add["MY_OTHER_VAR"] == actual_env_vars["MY_OTHER_VAR"]


def test_set_container_env_vars_removes_all_container_variables_except_path_and_sets_new_variables(
    control_client: ControlClient, valid_environment_with_env_vars: str
):
    # Arrange
    env_info = control_client.get_env_info(valid_environment_with_env_vars)
    cp_node = env_info.get_nodes(node_group="cp")[0]
    cp_node_id = cp_node.id

    vars_to_set = {"MY_FIRST_NEW_VAR": "value1", "MY_SECOND_NEW_VAR": "value2"}

    # Act
    control_client.set_container_env_vars(
        valid_environment_with_env_vars, vars=vars_to_set, node_id=cp_node_id
    )
    actual_env_vars = control_client.get_container_env_vars_by_group(
        valid_environment_with_env_vars, "cp"
    )

    # Assert
    assert "MY_JSON_VAR" not in actual_env_vars
    assert "MY_OTHER_VAR" not in actual_env_vars
    assert vars_to_set["MY_FIRST_NEW_VAR"] == actual_env_vars["MY_FIRST_NEW_VAR"]
    assert vars_to_set["MY_SECOND_NEW_VAR"] == actual_env_vars["MY_SECOND_NEW_VAR"]


def test_set_container_env_vars_by_group_removes_all_container_variables_except_path_and_sets_new_variables(
    control_client: ControlClient, valid_environment_with_env_vars: str
):
    # Arrange
    vars_to_set = {"MY_FIRST_NEW_VAR": "value1", "MY_SECOND_NEW_VAR": "value2"}

    # Act
    control_client.set_container_env_vars_by_group(
        valid_environment_with_env_vars, vars=vars_to_set, node_group="cp"
    )
    actual_env_vars = control_client.get_container_env_vars_by_group(
        valid_environment_with_env_vars, "cp"
    )

    # Assert
    assert "MY_JSON_VAR" not in actual_env_vars
    assert "MY_OTHER_VAR" not in actual_env_vars
    assert vars_to_set["MY_FIRST_NEW_VAR"] == actual_env_vars["MY_FIRST_NEW_VAR"]
    assert vars_to_set["MY_SECOND_NEW_VAR"] == actual_env_vars["MY_SECOND_NEW_VAR"]
