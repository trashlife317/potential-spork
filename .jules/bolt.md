## 2025-02-20 - Pre-calculation of Stable Notes
**Learning:** In `MelodyGenerator`, checking `is_stable_scale_degree` inside the generation loop (specifically for phrase endings) was a significant bottleneck. Pre-calculating this list in `__init__` reduced generation time by ~26%.
**Action:** Look for other invariant calculations inside loops that can be moved to initialization or pre-computed, especially those involving string parsing or multiple list lookups like `get_note_index`.

## 2025-02-20 - Optimized get_note_index
**Learning:** `get_note_index` was re-instantiating a dictionary and doing linear scans on every call. Pre-calculating a `NOTE_TO_INDEX` lookup table reduced execution time from ~1.35µs to ~0.19µs (~7x speedup).
**Action:** Whenever a function performs static lookups or normalizations, move the data structures to module scope.
