"""Tests for gameplay rules and interactions."""

from __future__ import annotations

import pygame

from src.core.collisions import refresh_doors_from_buttons, update_goal_state
from src.core.state import LevelProgress, Team
from src.entities.button import PressureButton
from src.entities.door import Door
from src.entities.goal import ExitGoal
from src.entities.hazard import is_character_safe_in_hazard
from src.entities.player import Player
from src.core.state import HazardKind


def _make_player(team: Team, x: int, y: int) -> Player:
    return Player(
        name=f"{team.value}_player",
        team=team,
        rect=pygame.Rect(x, y, 28, 34),
        color=(255, 255, 255),
    )


def test_hazard_compatibility_rules() -> None:
    assert is_character_safe_in_hazard(Team.FIRE, HazardKind.LAVA) is True
    assert is_character_safe_in_hazard(Team.FIRE, HazardKind.WATER) is False
    assert is_character_safe_in_hazard(Team.WATER, HazardKind.WATER) is True
    assert is_character_safe_in_hazard(Team.WATER, HazardKind.LAVA) is False
    assert is_character_safe_in_hazard(Team.FIRE, HazardKind.SLIME) is False
    assert is_character_safe_in_hazard(Team.WATER, HazardKind.SLIME) is False


def test_button_opens_linked_door() -> None:
    players = [_make_player(Team.FIRE, 40, 40), _make_player(Team.WATER, 400, 400)]
    button = PressureButton(
        button_id="button_a",
        rect=pygame.Rect(40, 40, 40, 40),
        linked_doors=("door_a",),
    )
    doors = {"door_a": Door(door_id="door_a", rect=pygame.Rect(120, 40, 40, 80))}

    refresh_doors_from_buttons([button], doors, players)
    assert button.is_pressed is True
    assert doors["door_a"].is_open is True


def test_win_condition_requires_both_exits() -> None:
    players = [_make_player(Team.FIRE, 10, 10), _make_player(Team.WATER, 80, 10)]
    exits = [
        ExitGoal(rect=pygame.Rect(0, 0, 50, 50), team=Team.FIRE),
        ExitGoal(rect=pygame.Rect(60, 0, 50, 50), team=Team.WATER),
    ]
    progress = LevelProgress()

    update_goal_state(players, exits, progress)
    assert players[0].reached_goal is True
    assert players[1].reached_goal is True
    assert progress.win is True
