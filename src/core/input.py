"""Input helpers and control mapping for local co-op."""

from __future__ import annotations

from dataclasses import dataclass

import pygame

from src.entities.player import Player


@dataclass(frozen=True, slots=True)
class ControlScheme:
    """Three-key control scheme for one player."""

    left: int
    right: int
    jump: int


def read_horizontal_axis(keys: pygame.key.ScancodeWrapper, scheme: ControlScheme) -> int:
    """Return horizontal intent as -1, 0, or 1."""
    return int(keys[scheme.right]) - int(keys[scheme.left])


def should_jump(keys: pygame.key.ScancodeWrapper, scheme: ControlScheme) -> bool:
    """Return True while jump key is held."""
    return bool(keys[scheme.jump])


def any_player_pressed(button_rect: pygame.Rect, players: list[Player]) -> bool:
    """Return True if any player overlaps button rect."""
    return any(button_rect.colliderect(player.rect) for player in players)
