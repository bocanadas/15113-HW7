"""Pygame entrypoint for Fireboy and Watergirl prototype."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pygame

from src.core.collisions import (
    check_hazards,
    collect_gems,
    refresh_doors_from_buttons,
    resolve_axis_collisions,
    update_goal_state,
)
from src.core.config import (
    COLOR_BG,
    DEFAULT_LEVEL_FILE,
    PLAYER_HEIGHT,
    PLAYER_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TARGET_FPS,
)
from src.core.input import ControlScheme, read_horizontal_axis, should_jump
from src.core.physics import apply_player_input, integrate_player, keep_in_bounds
from src.core.state import GameState, LevelProgress, Team
from src.entities.player import Player
from src.levels.loader import LevelData, load_level
from src.ui.hud import draw_hud
from src.ui.screens import draw_overlay_message


@dataclass(slots=True)
class RuntimeObjects:
    """Container for mutable game entities loaded from level data."""

    level_data: LevelData
    players: list[Player]
    world_rect: pygame.Rect


def _draw_brick_wall(surface: pygame.Surface) -> None:
    """Draw a temple-like brick wall background."""
    surface.fill((50, 57, 32))
    brick_h = 28
    brick_w = 64
    for row, y in enumerate(range(0, surface.get_height(), brick_h)):
        row_offset = 0 if row % 2 == 0 else brick_w // 2
        for x in range(-row_offset, surface.get_width(), brick_w):
            rect = pygame.Rect(x, y, brick_w, brick_h)
            pygame.draw.rect(surface, (62, 70, 40), rect)
            pygame.draw.rect(surface, (38, 44, 27), rect, width=1)

    for x in range(18, surface.get_width(), 120):
        for y in range(14, surface.get_height(), 96):
            pygame.draw.circle(surface, (190, 230, 190), (x, y), 1)


def _draw_vine(surface: pygame.Surface, start_x: int, start_y: int, length: int) -> None:
    """Draw one simple hanging vine."""
    points = []
    for i in range(length):
        px = start_x + (i % 4) - 2
        py = start_y + i * 6
        points.append((px, py))
    if len(points) > 1:
        pygame.draw.lines(surface, (50, 139, 53), False, points, 2)
    for index in range(0, len(points), 4):
        px, py = points[index]
        leaf_rect = pygame.Rect(px - 4, py - 3, 8, 6)
        pygame.draw.ellipse(surface, (70, 185, 72), leaf_rect)


def _draw_player_sprite(surface: pygame.Surface, player: Player) -> None:
    """Draw a clearer character silhouette with a face marker."""
    body = player.rect
    head = pygame.Rect(body.x + 4, body.y - 8, body.width - 8, 12)
    pygame.draw.rect(surface, player.color, body, border_radius=7)
    pygame.draw.ellipse(surface, player.color, head)
    pygame.draw.rect(surface, (255, 255, 255), body, width=2, border_radius=7)
    pygame.draw.ellipse(surface, (255, 255, 255), head, width=2)

    eye_color = (25, 25, 25)
    pygame.draw.circle(surface, eye_color, (head.centerx - 3, head.centery), 2)
    pygame.draw.circle(surface, eye_color, (head.centerx + 3, head.centery), 2)


def _build_runtime(level_file: Path) -> RuntimeObjects:
    level_data = load_level(level_file)
    fire_spawn = level_data.spawns[Team.FIRE]
    water_spawn = level_data.spawns[Team.WATER]

    players = [
        Player(
            name="Fireboy",
            team=Team.FIRE,
            rect=pygame.Rect(fire_spawn.x, fire_spawn.y, PLAYER_WIDTH, PLAYER_HEIGHT),
            color=(234, 91, 54),
        ),
        Player(
            name="Watergirl",
            team=Team.WATER,
            rect=pygame.Rect(water_spawn.x, water_spawn.y, PLAYER_WIDTH, PLAYER_HEIGHT),
            color=(72, 170, 255),
        ),
    ]
    world_rect = pygame.Rect(0, 0, level_data.world_width, level_data.world_height)
    return RuntimeObjects(level_data=level_data, players=players, world_rect=world_rect)


def _draw_level(surface: pygame.Surface, runtime: RuntimeObjects) -> None:
    level_data = runtime.level_data
    _draw_brick_wall(surface)
    for vine_x in (90, 220, 360, 520, 700, 840):
        _draw_vine(surface, vine_x, 0, 6)

    for solid in level_data.solid_tiles:
        pygame.draw.rect(surface, (148, 136, 92), solid, border_radius=4)
        pygame.draw.rect(surface, (181, 167, 118), solid, width=2, border_radius=4)
        # Step-like trim makes platforms easier to read.
        pygame.draw.line(surface, (94, 83, 53), (solid.left, solid.bottom - 2), (solid.right, solid.bottom - 2), 2)

    for door in level_data.doors.values():
        if not door.is_open:
            pygame.draw.rect(surface, (138, 136, 146), door.rect, border_radius=3)
            pygame.draw.rect(surface, (226, 226, 235), door.rect, width=2, border_radius=3)
            pygame.draw.circle(surface, (210, 196, 95), (door.rect.centerx, door.rect.centery), 5)

    hazard_colors = {
        "lava": (214, 82, 36),
        "water": (45, 120, 232),
        "slime": (88, 194, 82),
    }
    for hazard in level_data.hazards:
        base_color = hazard_colors[hazard.kind.value]
        glow_rect = hazard.rect.inflate(8, 4)
        pygame.draw.rect(surface, tuple(min(255, c + 30) for c in base_color), glow_rect, border_radius=4)
        pygame.draw.rect(surface, base_color, hazard.rect, border_radius=3)
        pygame.draw.rect(surface, (245, 245, 245), hazard.rect, width=1, border_radius=3)

    for button in level_data.buttons:
        color = (239, 212, 84) if button.is_pressed else (171, 147, 80)
        pygame.draw.rect(surface, color, button.rect, border_radius=8)
        pygame.draw.rect(surface, (65, 57, 32), button.rect, width=2, border_radius=8)

    for gem in level_data.gems:
        if gem.collected:
            continue
        color = (255, 130, 102) if gem.team == Team.FIRE else (112, 190, 255)
        gem_rect = gem.rect.inflate(-14, -14)
        pygame.draw.ellipse(surface, color, gem_rect)
        pygame.draw.ellipse(surface, (255, 255, 255), gem_rect, width=2)
        pygame.draw.ellipse(surface, (255, 255, 255), gem_rect.inflate(6, 6), width=1)

    for goal in level_data.exits:
        color = (232, 106, 79) if goal.team == Team.FIRE else (110, 173, 250)
        pygame.draw.rect(surface, color, goal.rect, border_radius=6)
        pygame.draw.rect(surface, (252, 252, 252), goal.rect, width=2, border_radius=6)
        # Team icon marker for readability.
        marker = "F" if goal.team == Team.FIRE else "W"
        marker_color = (35, 26, 22) if goal.team == Team.FIRE else (19, 32, 46)
        marker_font = pygame.font.SysFont("Georgia", 16, bold=True)
        marker_surface = marker_font.render(marker, True, marker_color)
        surface.blit(marker_surface, marker_surface.get_rect(center=goal.rect.center))

    for player in runtime.players:
        _draw_player_sprite(surface, player)


def run(level_file: Path = DEFAULT_LEVEL_FILE) -> None:
    """Start the game loop."""
    pygame.init()
    pygame.display.set_caption("Fireboy and Watergirl - Prototype")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 22)

    controls = {
        Team.FIRE: ControlScheme(left=pygame.K_a, right=pygame.K_d, jump=pygame.K_w),
        Team.WATER: ControlScheme(left=pygame.K_LEFT, right=pygame.K_RIGHT, jump=pygame.K_UP),
    }

    runtime = _build_runtime(level_file)
    state = GameState(current_level_name=runtime.level_data.level_id)
    state.progress = LevelProgress(total_gems=len(runtime.level_data.gems))
    jump_latch = {Team.FIRE: False, Team.WATER: False}
    running = True

    while running:
        dt = clock.tick(TARGET_FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                runtime = _build_runtime(level_file)
                state.progress = LevelProgress(total_gems=len(runtime.level_data.gems))
                jump_latch = {Team.FIRE: False, Team.WATER: False}

        if not state.progress.game_over and not state.progress.win:
            keys = pygame.key.get_pressed()
            dynamic_solids = list(runtime.level_data.solid_tiles)
            dynamic_solids.extend(door.rect for door in runtime.level_data.doors.values() if door.blocking)

            for player in runtime.players:
                scheme = controls[player.team]
                axis = read_horizontal_axis(keys, scheme)
                jump_held = should_jump(keys, scheme)
                do_jump = jump_held and not jump_latch[player.team]
                apply_player_input(player, axis, do_jump)
                jump_latch[player.team] = jump_held

                player.rect.x += int(player.velocity.x * dt)
                resolve_axis_collisions(player, dynamic_solids, axis="x")
                player.on_ground = False
                integrate_player(player, dt)
                resolve_axis_collisions(player, dynamic_solids, axis="y")
                keep_in_bounds(player, runtime.world_rect)
                if player.rect.bottom > runtime.world_rect.bottom + 5:
                    state.progress.game_over = True
                    state.progress.status_message = f"{player.name} fell out of bounds."

            refresh_doors_from_buttons(runtime.level_data.buttons, runtime.level_data.doors, runtime.players)
            collect_gems(runtime.players, runtime.level_data.gems, state.progress)
            check_hazards(runtime.players, runtime.level_data.hazards, state.progress)
            update_goal_state(runtime.players, runtime.level_data.exits, state.progress)
            if state.progress.game_over:
                state.progress.status_message = state.progress.status_message or "Game over."
            if state.progress.win:
                state.progress.status_message = "Level complete. Press R to replay."

        screen.fill(COLOR_BG)
        _draw_level(screen, runtime)
        draw_hud(screen, font, state.progress, len(runtime.level_data.gems))
        if state.progress.game_over:
            draw_overlay_message(screen, font, "Game over - press R to retry")
        elif state.progress.win:
            draw_overlay_message(screen, font, "You win! Press R to replay")
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    run()
