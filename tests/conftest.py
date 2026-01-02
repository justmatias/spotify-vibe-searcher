from typing import Any

import pytest

pytest_plugins = ["tests.conftest_polyfactory"]


@pytest.fixture(scope="module")
def vcr_config() -> dict[str, Any]:
    return {
        "filter_headers": [("Authorization", "Bearer MOCKED_TOKEN")],
        "filter_query_parameters": [("access_token", "MOCKED_TOKEN")],
        "ignore_localhost": False,
        "record_mode": "once",
    }
