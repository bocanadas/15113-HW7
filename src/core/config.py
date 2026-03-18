"""Global configuration constants for the game."""

from __future__ import annotations

from pathlib import Path

# Display and timing
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 640
TARGET_FPS = 60
GRAVITY = 1800.0

# Tile/grid
TILE_SIZE = 40

# Player tuning
PLAYER_WIDTH = 28
PLAYER_HEIGHT = 34
PLAYER_SPEED = 230.0
PLAYER_JUMP_VELOCITY = -760.0

# Rendering
COLOR_BG = (22, 24, 31)
COLOR_TEXT = (245, 245, 245)

# Paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
LEVELS_DIR = PROJECT_ROOT / "src" / "levels"
DEFAULT_LEVEL_FILE = LEVELS_DIR / "level_01.json"
