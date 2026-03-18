"""Goal and collectible entities."""

from __future__ import annotations

from dataclasses import dataclass

import pygame

from src.core.state import Team


@dataclass(slots=True)
class ExitGoal:
    """Exit tile for one specific character team."""

    rect: pygame.Rect
    team: Team


@dataclass(slots=True)
class Gem:
    """Collectible gem linked to one team."""

    rect: pygame.Rect
    team: Team
    collected: bool = False
