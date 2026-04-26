"""
Pytest configuration and fixtures for CyberSecSuite Core MCP tests.

Provides shared fixtures, setup/teardown logic, and configuration
for the test suite. All fixtures follow async/await patterns for proper
event loop management.
"""

import asyncio
import logging
from typing import Any, Generator

import pytest

# Configure logging for tests
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """
    Create an event loop for the test session.

    Yields:
        asyncio.AbstractEventLoop: Event loop for async tests
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()

    yield loop
    loop.close()


@pytest.fixture
def mock_config() -> dict[str, Any]:
    """
    Provide mock configuration for csscore tests.

    Returns:
        dict: Mock configuration dictionary
    """
    return {
        "logging": {"level": "DEBUG", "format": "json"},
        "marketplace": {"cache_ttl": 3600, "registry_url": "local"},
    }


# Markers for test categorization
def pytest_configure(config: pytest.Config) -> None:
    """
    Register custom pytest markers.

    Args:
        config: pytest configuration object
    """
    config.addinivalue_line(
        "markers",
        "asyncio: mark test as async (requires pytest-asyncio)",
    )
    config.addinivalue_line(
        "markers",
        "integration: mark test as integration test",
    )
    config.addinivalue_line(
        "markers",
        "unit: mark test as unit test",
    )
