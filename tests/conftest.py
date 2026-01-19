"""Pytest configuration and fixtures."""

import pytest
import respx


@pytest.fixture
def respx_mock() -> respx.MockRouter:
    """Fixture to provide a respx mock router for each test."""
    with respx.mock() as respx_mock_router:
        yield respx_mock_router
