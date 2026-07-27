"""
Pytest configuration for the test suite.

By default, tests marked with @pytest.mark.slow are skipped.
Run with --slow flag to include them:  pytest --slow
"""

# pyrefly: ignore [missing-import]
import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--slow",
        action="store_true",
        default=False,
        help="Run slow integration tests that hit disk or the network.",
    )


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line(
        "markers",
        "slow: mark test as slow (loads large graph files or makes network requests).",
    )


def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    if config.getoption("--slow"):
        return  # --slow given: run everything

    skip_slow = pytest.mark.skip(reason="slow test – run with --slow to enable")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)
