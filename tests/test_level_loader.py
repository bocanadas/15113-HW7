"""Tests for JSON level loading."""

from __future__ import annotations

from pathlib import Path

from src.core.config import TILE_SIZE
from src.core.state import Team
from src.levels.loader import load_level


def test_load_level_has_required_actors() -> None:
    level = load_level(Path("src/levels/level_01.json"))
    assert level.level_id == "level_01"
    assert Team.FIRE in level.spawns
    assert Team.WATER in level.spawns
    assert len(level.solid_tiles) > 0
    assert len(level.gems) == 2


def test_world_dimensions_respect_tile_size() -> None:
    level = load_level(Path("src/levels/level_01.json"))
    assert level.world_width == 24 * TILE_SIZE
    assert level.world_height == 16 * TILE_SIZE
