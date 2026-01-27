## 2025-02-20 - Pre-calculation of Stable Notes
**Learning:** In `MelodyGenerator`, checking `is_stable_scale_degree` inside the generation loop (specifically for phrase endings) was a significant bottleneck. Pre-calculating this list in `__init__` reduced generation time by ~26%.
**Action:** Look for other invariant calculations inside loops that can be moved to initialization or pre-computed, especially those involving string parsing or multiple list lookups like `get_note_index`.

## 2025-02-21 - Pre-computed Note Index Map
**Learning:** `get_note_index` in `src/music_theory.py` relied on runtime string normalization and linear list search, costing ~1.36µs per call. Replacing this with a pre-computed hash map `NOTE_TO_INDEX` reduced execution time to ~0.11µs (>12x speedup).
**Action:** Favor static hash maps over dynamic string manipulation for frequent lookups involving finite sets of keys (like musical notes).
