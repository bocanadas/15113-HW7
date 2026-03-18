"""Level loading from JSON files."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import pygame

from src.core.config import TILE_SIZE
from src.core.state import HazardKind, Team
from src.entities.button import PressureButton
from src.entities.door import Door
from src.entities.goal import ExitGoal, Gem
from src.entities.hazard import Hazard


@dataclass(slots=True)
class SpawnPoint:
    """Spawn location for one character."""

    team: Team
    x: int
    y: int


@dataclass(slots=True)
class LevelData:
    """Fully parsed level data."""

    level_id: str
    world_width: int
    world_height: int
    solid_tiles: list[pygame.Rect]
    hazards: list[Hazard]
    doors: dict[str, Door]
    buttons: list[PressureButton]
    exits: list[ExitGoal]
    gems: list[Gem]
    spawns: dict[Team, SpawnPoint]


def _rect_from_tile(tile_x: int, tile_y: int, width: int = 1, height: int = 1) -> pygame.Rect:
    return pygame.Rect(tile_x * TILE_SIZE, tile_y * TILE_SIZE, width * TILE_SIZE, height * TILE_SIZE)


def load_level(path: Path) -> LevelData:
    """Parse and validate a level JSON file."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    world = raw["world"]
    world_width = int(world["tiles_wide"]) * TILE_SIZE
    world_height = int(world["tiles_high"]) * TILE_SIZE

    solid_tiles = [
        _rect_from_tile(tile["x"], tile["y"], tile.get("w", 1), tile.get("h", 1)) for tile in raw["solids"]
    ]

    hazards = [
        Hazard(
            rect=_rect_from_tile(h["x"], h["y"], h.get("w", 1), h.get("h", 1)),
            kind=HazardKind(h["kind"]),
        )
        for h in raw["hazards"]
    ]

    doors: dict[str, Door] = {}
    for door in raw["doors"]:
        door_id = str(door["id"])
        doors[door_id] = Door(
            door_id=door_id,
            rect=_rect_from_tile(door["x"], door["y"], door.get("w", 1), door.get("h", 1)),
            initially_open=bool(door.get("initially_open", False)),
        )

    buttons = [
        PressureButton(
            button_id=str(button["id"]),
            rect=_rect_from_tile(button["x"], button["y"], button.get("w", 1), button.get("h", 1)),
            linked_doors=tuple(str(door_id) for door_id in button["linked_doors"]),
        )
        for button in raw["buttons"]
    ]

    exits = [
        ExitGoal(
            rect=_rect_from_tile(goal["x"], goal["y"], goal.get("w", 1), goal.get("h", 1)),
            team=Team(goal["team"]),
        )
        for goal in raw["exits"]
    ]

    gems = [
        Gem(
            rect=_rect_from_tile(gem["x"], gem["y"]),
            team=Team(gem["team"]),
        )
        for gem in raw["gems"]
    ]

    spawns = {
        Team(spawn["team"]): SpawnPoint(
            team=Team(spawn["team"]),
            x=int(spawn["x"]) * TILE_SIZE,
            y=int(spawn["y"]) * TILE_SIZE,
        )
        for spawn in raw["spawns"]
    }
    if Team.FIRE not in spawns or Team.WATER not in spawns:
        raise ValueError("Both fire and water spawn points are required.")

    return LevelData(
        level_id=str(raw["id"]),
        world_width=world_width,
        world_height=world_height,
        solid_tiles=solid_tiles,
        hazards=hazards,
        doors=doors,
        buttons=buttons,
        exits=exits,
        gems=gems,
        spawns=spawns,
    )
