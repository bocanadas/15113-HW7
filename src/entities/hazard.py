"""Hazard entity and elemental compatibility rules."""

from __future__ import annotations

from dataclasses import dataclass

import pygame

from src.core.state import HazardKind, Team


@dataclass(slots=True)
class Hazard:
    """Rectangular hazard zone."""

    rect: pygame.Rect
    kind: HazardKind


def is_character_safe_in_hazard(team: Team, hazard_kind: HazardKind) -> bool:
    """Return whether a team survives while touching a hazard."""
    if hazard_kind == HazardKind.SLIME:
        return False
    if hazard_kind == HazardKind.LAVA:
        return team == Team.FIRE
    if hazard_kind == HazardKind.WATER:
        return team == Team.WATER
    return False
