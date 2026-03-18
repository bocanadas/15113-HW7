"""Shared game state data structures."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Team(str, Enum):
    """Element team for characters and interactables."""

    FIRE = "fire"
    WATER = "water"


class HazardKind(str, Enum):
    """Hazard tile types."""

    LAVA = "lava"
    WATER = "water"
    SLIME = "slime"


@dataclass(slots=True)
class LevelProgress:
    """Run-time progress values tracked per level run."""

    gems_collected: int = 0
    total_gems: int = 0
    game_over: bool = False
    win: bool = False
    status_message: str = ""


@dataclass(slots=True)
class GameState:
    """Top-level game state for active gameplay."""

    current_level_name: str = "level_01"
    progress: LevelProgress = field(default_factory=LevelProgress)
