## 2025-02-20 - Pre-calculation of Stable Notes
**Learning:** In `MelodyGenerator`, checking `is_stable_scale_degree` inside the generation loop (specifically for phrase endings) was a significant bottleneck. Pre-calculating this list in `__init__` reduced generation time by ~26%.
**Action:** Look for other invariant calculations inside loops that can be moved to initialization or pre-computed, especially those involving string parsing or multiple list lookups like `get_note_index`.

## 2025-02-21 - Optimized Note Lookup
**Learning:** `get_note_index` in `music_theory.py` was re-parsing strings and creating temporary dictionaries on every call. Replacing this with a static `NOTE_TO_INDEX` lookup table improved performance by ~11x.
**Action:** Identify other "leaf" utility functions that perform redundant object creation or string parsing and replace them with static lookup tables where possible.
