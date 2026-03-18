"""Physics update helpers."""

from __future__ import annotations

import pygame

from src.core.config import GRAVITY, PLAYER_JUMP_VELOCITY, PLAYER_SPEED
from src.entities.player import Player


def apply_player_input(player: Player, horizontal_axis: int, jump_pressed: bool) -> None:
    """Apply movement intent to velocity."""
    player.velocity.x = horizontal_axis * PLAYER_SPEED
    if jump_pressed and player.on_ground:
        player.velocity.y = PLAYER_JUMP_VELOCITY
        player.on_ground = False


def integrate_player(player: Player, dt: float) -> None:
    """Integrate velocity and position with gravity."""
    player.velocity.y += GRAVITY * dt
    player.rect.y += int(player.velocity.y * dt)


def keep_in_bounds(player: Player, world_rect: pygame.Rect) -> None:
    """Clamp player inside world bounds."""
    player.rect.left = max(player.rect.left, world_rect.left)
    player.rect.right = min(player.rect.right, world_rect.right)
