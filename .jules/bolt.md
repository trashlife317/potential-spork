## 2025-02-20 - Pre-calculation of Stable Notes
**Learning:** In `MelodyGenerator`, checking `is_stable_scale_degree` inside the generation loop (specifically for phrase endings) was a significant bottleneck. Pre-calculating this list in `__init__` reduced generation time by ~26%.
**Action:** Look for other invariant calculations inside loops that can be moved to initialization or pre-computed, especially those involving string parsing or multiple list lookups like `get_note_index`.

## 2025-02-21 - Optimization of get_note_index
**Learning:** Replacing dynamic dictionary creation and list searches with a static O(1) lookup table in `get_note_index` improved execution speed by ~9.6x (1.26µs -> 0.13µs).
**Action:** Always prefer module-level static constants for lookup tables over defining them inside frequently called functions.
