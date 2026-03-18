"""Helpers for centered overlay messages."""

from __future__ import annotations

import pygame

from src.core.config import COLOR_TEXT


def draw_overlay_message(surface: pygame.Surface, font: pygame.font.Font, message: str) -> None:
    """Draw a semi-transparent center message box."""
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 120))
    surface.blit(overlay, (0, 0))

    text = font.render(message, True, COLOR_TEXT)
    text_rect = text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
    surface.blit(text, text_rect)
