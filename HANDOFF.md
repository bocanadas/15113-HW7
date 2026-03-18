# Handoff Notes

## Current Completion State
- Core vertical slice is playable with two characters.
- Co-op gate puzzle, hazards, exits, and restart loop are implemented.
- Basic tests pass (`5 passed`).

## Environment Setup (Use Venv Only)
- Create local venv: `python3 -m venv .venv`
- Activate (macOS/Linux): `source .venv/bin/activate`
- Install deps: `python -m pip install -r requirements.txt`
- Run game/tests in venv: `python -m src.main`, `python -m pytest -q`
- Do not install dependencies globally for this project.

## Remaining Work To Finish Application
1. Add at least two new levels (`level_02.json`, `level_03.json`).
2. Add two advanced mechanics:
   - Moving platforms
   - Lasers with toggle switches
3. Add polish:
   - Audio effects and background music
   - Win/lose transition screens with small animations
   - Visual style target: temple-ruin environment, moss/stone texture feel, red-vs-blue character readability, glowing gems/hazards
   - Use `assets/style-reference.png` as the look target

## Known Gaps / Edge Cases
- No camera system; map must fit screen bounds.
- No sprite assets yet (rectangles only).
- No save/load progression between levels.

## How To Continue Safely
- Keep constants in `src/core/config.py`.
- Extend rules in `src/core/collisions.py` and add tests in `tests/`.
- Add new level files without changing loader schema when possible.

## Suggested Roadmap
1. Implement mechanic scaffolds in `src/entities/` + `src/core/`.
2. Create two new level JSON files exercising those mechanics.
3. Add transitions and audio in `src/ui/` and `src/main.py`.
4. Expand tests for each new mechanic before adding more content.
