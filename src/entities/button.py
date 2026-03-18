"""Pressure button entity that controls doors."""

from __future__ import annotations

from dataclasses import dataclass

import pygame


@dataclass(slots=True)
class PressureButton:
    """Button activated while any player stands on it."""

    button_id: str
    rect: pygame.Rect
    linked_doors: tuple[str, ...]
    is_pressed: bool = False
