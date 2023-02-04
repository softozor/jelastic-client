from typing import Dict

import pytest

from jelastic_client import get_manifest_data


@pytest.mark.parametrize(
    "properly_formatted_success_text,expected_dict",
    [
        (
            """<strong>field1</strong>: value1<br />
<strong>field2</strong>: value2""",
            {"field1": "value1", "field2": "value2"},
        ),
        (
            """field1: value1<br />
field2: value2""",
            {"field1": "value1", "field2": "value2"},
        ),
        ("", {}),
    ],
)
def test_get_manifest_data_from_properly_formatted_success_text_returns_expected_dict(
    properly_formatted_success_text: str, expected_dict: Dict[str, str]
):
    # Arrange

    # Act
    actual_dict = get_manifest_data(properly_formatted_success_text)

    # Assert
    assert actual_dict == expected_dict


@pytest.mark.parametrize(
    "improperly_formatted_success_text,expected_dict",
    [
        (
            """<i>field1</i>: value1<br />
        <p>field2: value2
    """,
            {"<i>field1</i>": "value1", "        <p>field2": "value2"},
        ),
    ],
)
def test_get_manifest_data_from_improperly_formatted_text_returns_improper_dict(
    improperly_formatted_success_text: str, expected_dict: Dict[str, str]
):
    # Arrange
    properly_formatted_success_text = """<i>field1</i>: value1<br />
        <p>field2: value2
    """

    expected_dict = {"<i>field1</i>": "value1", "        <p>field2": "value2"}

    # Act
    actual_dict = get_manifest_data(properly_formatted_success_text)

    # Assert
    assert actual_dict == expected_dict
