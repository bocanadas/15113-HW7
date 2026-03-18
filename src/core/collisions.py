"""Collision resolution and gameplay rule checks."""

from __future__ import annotations

import pygame

from src.core.state import LevelProgress
from src.entities.button import PressureButton
from src.entities.door import Door
from src.entities.goal import ExitGoal, Gem
from src.entities.hazard import Hazard, is_character_safe_in_hazard
from src.entities.player import Player


def resolve_axis_collisions(player: Player, solids: list[pygame.Rect], axis: str) -> None:
    """Resolve collisions for one axis after motion."""
    for solid in solids:
        if not player.rect.colliderect(solid):
            continue
        if axis == "x":
            if player.velocity.x > 0:
                player.rect.right = solid.left
            elif player.velocity.x < 0:
                player.rect.left = solid.right
            player.velocity.x = 0.0
            continue
        if player.velocity.y > 0:
            player.rect.bottom = solid.top
            player.on_ground = True
        elif player.velocity.y < 0:
            player.rect.top = solid.bottom
        player.reset_vertical_motion()


def refresh_doors_from_buttons(buttons: list[PressureButton], doors: dict[str, Door], players: list[Player]) -> None:
    """Open doors while linked buttons are pressed."""
    pressed_by_id = {button.button_id: False for button in buttons}
    for button in buttons:
        button.is_pressed = any(button.rect.colliderect(player.rect) for player in players)
        pressed_by_id[button.button_id] = button.is_pressed

    door_open_map = {door_id: False for door_id in doors}
    for button in buttons:
        if not pressed_by_id[button.button_id]:
            continue
        for linked_door_id in button.linked_doors:
            if linked_door_id in door_open_map:
                door_open_map[linked_door_id] = True

    for door_id, door in doors.items():
        door.is_open = door.initially_open or door_open_map[door_id]


def check_hazards(players: list[Player], hazards: list[Hazard], progress: LevelProgress) -> None:
    """Mark game over if any player touches an incompatible hazard."""
    for player in players:
        for hazard in hazards:
            if not player.rect.colliderect(hazard.rect):
                continue
            if not is_character_safe_in_hazard(player.team, hazard.kind):
                progress.game_over = True
                progress.status_message = f"{player.name} was eliminated by {hazard.kind.value}."
                return


def collect_gems(players: list[Player], gems: list[Gem], progress: LevelProgress) -> None:
    """Collect overlapping gems and update score-style progress."""
    for gem in gems:
        if gem.collected:
            continue
        for player in players:
            if player.team == gem.team and player.rect.colliderect(gem.rect):
                gem.collected = True
                progress.gems_collected += 1
                break


def update_goal_state(players: list[Player], exits: list[ExitGoal], progress: LevelProgress) -> None:
    """Set per-player goal status and mark level win."""
    for player in players:
        player.reached_goal = any(
            goal.team == player.team and player.rect.colliderect(goal.rect) for goal in exits
        )
    if all(player.reached_goal for player in players):
        progress.win = True
        progress.status_message = "Level complete."
