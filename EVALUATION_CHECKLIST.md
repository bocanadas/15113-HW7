# Evaluation Checklist (Handoff-Ready)

Mark each item PASS/FAIL before handoff.

## Playability
- [ ] Game launches from `python3 -m src.main`
- [ ] Both players can move and jump reliably
- [ ] Restart (`R`) resets level and state cleanly

## Co-op Mechanics
- [ ] At least one puzzle requires both players (button + door + dual exits)
- [ ] Win only occurs when both teams reach matching exits

## Rule Correctness
- [ ] Fireboy survives lava, fails in water/slime
- [ ] Watergirl survives water, fails in lava/slime
- [ ] Gem collection matches player team rules

## Reliability
- [ ] `python3 -m pytest -q` passes
- [ ] No obvious frame stutter in a full manual run

## Handoff Quality
- [ ] README is concise and clear (quickstart + exact finish tasks)
- [ ] HANDOFF file lists remaining work, known gaps, and roadmap
- [ ] Remaining tasks are documented, not half-implemented
