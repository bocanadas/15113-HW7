"""HUD rendering helpers."""

from __future__ import annotations

import pygame

from src.core.config import COLOR_TEXT
from src.core.state import LevelProgress


def draw_hud(
    surface: pygame.Surface,
    font: pygame.font.Font,
    progress: LevelProgress,
    total_gems: int,
) -> None:
    """Draw controls and progress text."""
    panel = pygame.Rect(10, 10, 470, 110)
    panel_surface = pygame.Surface((panel.width, panel.height), pygame.SRCALPHA)
    panel_surface.fill((20, 24, 18, 170))
    surface.blit(panel_surface, panel.topleft)
    pygame.draw.rect(surface, (215, 182, 88), panel, width=2, border_radius=8)

    lines = [
        "Fireboy: A/D + W",
        "Watergirl: Left/Right + Up",
        "Objective: hold button, collect gems, both reach exits",
        f"Gems: {progress.gems_collected}/{total_gems}",
    ]
    if progress.status_message:
        lines.append(progress.status_message)

    for index, line in enumerate(lines):
        color = COLOR_TEXT if index < 3 else (255, 224, 137)
        text = font.render(line, True, color)
        surface.blit(text, (22, 20 + index * 23))
