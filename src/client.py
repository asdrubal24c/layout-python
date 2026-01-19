"""Async client for the Rick and Morty API."""

from __future__ import annotations

from typing import Any

import httpx

from src.models import Character

BASE_URL = "https://rickandmortyapi.com/api"


class RickAndMortyClient:
    """Async client for interacting with the Rick and Morty API."""

    def __init__(self, timeout: float = 10.0, base_url: str = BASE_URL) -> None:
        """Initialize the client.

        Args:
            timeout: Request timeout in seconds. Defaults to 10.0.
            base_url: Base URL for the API. Defaults to BASE_URL.
        """
        self._base_url = base_url
        self._client = httpx.AsyncClient(timeout=timeout)

    async def get_character(self, character_id: int) -> Character:
        """Get a character by ID.

        Args:
            character_id: The ID of the character to retrieve.

        Returns:
            A Character model instance.

        Raises:
            httpx.HTTPStatusError: If the API returns an error status code.
            httpx.RequestError: If the request fails.
        """
        url = f"{self._base_url}/character/{character_id}"
        response = await self._client.get(url)
        response.raise_for_status()
        json_data: dict[str, Any] = response.json()
        return Character.model_validate(json_data)

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()

    async def __aenter__(self) -> RickAndMortyClient:
        """Async context manager entry."""
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any,
    ) -> None:
        """Async context manager exit."""
        await self.close()
