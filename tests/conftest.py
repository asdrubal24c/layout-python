"""Pytest configuration and fixtures."""

from collections.abc import Generator

import pytest
import respx


@pytest.fixture
def respx_mock() -> Generator[respx.MockRouter, None, None]:
    """Fixture to provide a respx mock router for each test."""
    with respx.mock() as respx_mock_router:
        yield respx_mock_router
