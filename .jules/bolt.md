## 2025-02-20 - Pre-calculation of Stable Notes
**Learning:** In `MelodyGenerator`, checking `is_stable_scale_degree` inside the generation loop (specifically for phrase endings) was a significant bottleneck. Pre-calculating this list in `__init__` reduced generation time by ~26%.
**Action:** Look for other invariant calculations inside loops that can be moved to initialization or pre-computed, especially those involving string parsing or multiple list lookups like `get_note_index`.

## 2025-02-20 - Pre-computation of Lookup Tables
**Learning:** Replacing repeated string normalization and linear list searches with a pre-computed dictionary lookup reduced execution time by ~14x (1.7μs -> 0.12μs) for critical path functions like `get_note_index`.
**Action:** Identify frequent low-level helper functions that perform redundant normalization or searching and refactor them to use static lookup tables.
