"""Pydantic models for Rick and Morty API responses."""

from __future__ import annotations

from pydantic import BaseModel, Field, HttpUrl


class CharacterOrigin(BaseModel):
    """Model for character origin information."""

    name: str
    url: HttpUrl


class CharacterLocation(BaseModel):
    """Model for character location information."""

    name: str
    url: HttpUrl


class Character(BaseModel):
    """Model for a Rick and Morty character."""

    id: int
    name: str
    status: str
    species: str
    type: str
    gender: str
    origin: CharacterOrigin
    location: CharacterLocation
    image: HttpUrl
    episode: list[HttpUrl] = Field(default_factory=list)
    url: HttpUrl
    created: str  # ISO datetime string

    class Config:
        """Pydantic configuration."""

        frozen = True
        str_strip_whitespace = True
