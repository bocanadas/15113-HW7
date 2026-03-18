# Fireboy and Watergirl (Pygame Prototype)

## 1) Quickstart
- Create venv (project-local): `python3 -m venv .venv`
- Activate venv (macOS/Linux): `source .venv/bin/activate`
- Activate venv (Windows PowerShell): `.venv\Scripts\Activate.ps1`
- Install dependencies inside venv: `python -m pip install -r requirements.txt`
- Run game: `python -m src.main`
- Run tests: `python -m pytest -q`

## 2) Controls
- Fireboy: `A`/`D` move, `W` jump
- Watergirl: `Left`/`Right` move, `Up` jump
- Restart level: `R`

## 3) What Is Implemented Now
- Two-player local controls on one keyboard
- Tile-based collision and gravity platforming
- Element hazards: lava, water, slime (team-specific safety rules)
- Button -> door cooperative interaction
- Team-matched exits and win condition
- Team-matched gem collection

## 4) Architecture (Where To Edit)
- `src/main.py`: loop, rendering, high-level gameplay flow
- `src/core/`: config, input, physics, collision/game rule updates
- `src/entities/`: dataclass models for players and interactables
- `src/levels/`: JSON level files + loader
- `src/ui/`: HUD and overlay messaging

## 5) Finish Checklist (Priority Order)
- Add `level_02.json` and `level_03.json` with stronger co-op puzzles
- Implement 2 advanced mechanics from `HANDOFF.md`
- Add polish (audio, transitions, art pass)
- Match the target style (temple ruins, earthy palette, bright red/blue player contrast, gem glow)
- Expand automated tests for new mechanics

## 6) Notes For Handoff
- Keep level content data-driven in `src/levels/*.json`
- Do not rewrite core architecture; extend existing modules
- Any partially started task must be tagged with a clear `TODO(owner):` note
- Keep dependency installs inside `.venv` only (avoid global Python installs)
- Match visuals to `assets/style-reference.png` for final art direction