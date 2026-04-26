"""
Pytest configuration and fixtures for MCP Template tests.

This module provides shared fixtures, setup/teardown logic, and configuration
for the test suite. All fixtures follow async/await patterns for proper
event loop management.
"""

import asyncio
import logging
from typing import Any, AsyncGenerator, Generator

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
async def async_client() -> AsyncGenerator[Any, None]:
    """
    Create an async HTTP client for testing.
    
    This is a template fixture. Replace with actual async HTTP client
    (e.g., httpx.AsyncClient) for your specific implementation.
    
    Yields:
        Async client instance
    """
    # TODO: Initialize async HTTP client
    client = None
    
    yield client
    
    # TODO: Clean up client resources
    if client is not None:
        await asyncio.sleep(0)  # Placeholder for cleanup


@pytest.fixture
def mock_config() -> dict[str, Any]:
    """
    Provide mock configuration for tests.
    
    Returns:
        dict: Mock configuration dictionary
    """
    return {
        "debug": True,
        "log_level": "DEBUG",
        "host": "localhost",
        "port": 8000,
    }


@pytest.fixture
async def sample_data() -> dict[str, Any]:
    """
    Provide sample data for testing.
    
    Returns:
        dict: Sample test data
    """
    return {
        "sample_id": "test-001",
        "sample_name": "Test Sample",
        "timestamp": "2024-01-01T00:00:00Z",
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
