"""Player entity for Fireboy/Watergirl characters."""

from __future__ import annotations

from dataclasses import dataclass, field

import pygame

from src.core.state import Team


@dataclass(slots=True)
class Player:
    """A controllable character with platformer movement state."""

    name: str
    team: Team
    rect: pygame.Rect
    color: tuple[int, int, int]
    velocity: pygame.Vector2 = field(default_factory=pygame.Vector2)
    on_ground: bool = False
    reached_goal: bool = False

    def reset_vertical_motion(self) -> None:
        """Stop vertical movement after landing/hitting ceiling."""
        self.velocity.y = 0.0
