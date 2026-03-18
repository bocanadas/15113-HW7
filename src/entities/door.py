"""Door entity controlled by level buttons."""

from __future__ import annotations

from dataclasses import dataclass

import pygame


@dataclass(slots=True)
class Door:
    """Solid obstacle that can be toggled open or closed."""

    door_id: str
    rect: pygame.Rect
    initially_open: bool = False
    is_open: bool = False

    def __post_init__(self) -> None:
        self.is_open = self.initially_open

    @property
    def blocking(self) -> bool:
        """Whether this door should block movement."""
        return not self.is_open
